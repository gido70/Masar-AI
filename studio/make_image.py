#!/usr/bin/env python3
"""تعديل صورة المقدّم عبر WaveSpeed (مثلًا تغيير اللبس لكل وحدة).

التشغيل: python studio/make_image.py <اسم مجلد الإنتاج>
يقرأ productions/<الإنتاج>/image.json:
  {"model": "google/nano-banana-2/edit", "image": "studio/assets/presenter-screen.png",
   "cost_each": 0.07, "variants": [{"prompt": "...", "output": "presenter-a.png"}, ...]}
الضوابط: لا يولّد ملفًا موجودًا · حد للتكلفة MAX_TOTAL · مهلة · المفتاح من البيئة فقط.
كل ناتج يُوحَّد إلى 1280×720 (قص من الوسط) ليطابق صورة المقدّم الأصلية.
"""
import json, os, sys, time, urllib.request
from PIL import Image, ImageOps

API = 'https://api.wavespeed.ai/api/v3'
MAX_TOTAL = float(os.environ.get('MAX_TOTAL', 1.0)); TIMEOUT = 15 * 60

def call(method, url, key, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())

def raw_url(path):
    return f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{os.environ['GITHUB_SHA']}/{path}"

def main(name):
    key = os.environ.get('WAVESPEED_API_KEY') or sys.exit('✗ WAVESPEED_API_KEY غير موجود')
    base = f'productions/{name}'; cfg = json.load(open(f'{base}/image.json', encoding='utf-8'))
    todo = [v for v in cfg['variants'] if not os.path.exists(f"{base}/{v['output']}")]
    total = len(todo) * cfg.get('cost_each', 0.07)
    print(f'{len(todo)} صورة ← تقدير {total:.2f} دولار (الحد {MAX_TOTAL:.2f})')
    if total > MAX_TOTAL: sys.exit('✗ التكلفة أعلى من الحد.')
    for v in todo:
        r = call('POST', f"{API}/{cfg['model']}", key, {'images': [raw_url(cfg['image'])], 'prompt': v['prompt']})
        pid = (r.get('data') or {}).get('id') or sys.exit(f'✗ لا رقم: {r}')
        print(f"→ {v['output']} (رقم {pid})"); t0 = time.time()
        while True:
            time.sleep(5); st = call('GET', f'{API}/predictions/{pid}/result', key).get('data') or {}
            if st.get('status') == 'completed': break
            if st.get('status') in ('failed', 'cancelled', 'timeout', 'deleted'): sys.exit(f"✗ فشل: {st.get('error')}")
            if time.time() - t0 > TIMEOUT: sys.exit('✗ تجاوز المهلة')
        url = (st.get('outputs') or [None])[0] or sys.exit('✗ بلا ناتج')
        tmp = f"{base}/_tmp_{v['output']}"; urllib.request.urlretrieve(url, tmp)
        im = ImageOps.fit(Image.open(tmp).convert('RGB'), (1280, 720), Image.LANCZOS); im.save(f"{base}/{v['output']}"); os.remove(tmp)
        print(f"✓ {v['output']}")

if __name__ == '__main__':
    main(sys.argv[1])
