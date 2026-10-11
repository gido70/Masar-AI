#!/usr/bin/env python3
"""مقاطع المقدّم تلقائيًا عبر WaveSpeed InfiniteTalk (المرحلة 3).

التشغيل: python studio/make_presenter.py <اسم مجلد الإنتاج>
يقرأ productions/<الإنتاج>/presenter.json:
  {"image": "studio/assets/presenter-screen.png", "resolution": "720p",
   "clips": [{"audio": "narration-open.mp3", "output": "presenter-open.mp4"}, ...]}

الضوابط: لا يولّد مقطعًا موجودًا · يرفض أي صوت أطول من MAX_SECONDS · يرفض إن تجاوزت
التكلفة التقديرية MAX_TOTAL · مهلة قصوى للانتظار · المفتاح من متغير البيئة WAVESPEED_API_KEY فقط.
"""
import json, math, os, subprocess, sys, time, urllib.request, urllib.error

API = 'https://api.wavespeed.ai/api/v3'
MODEL = 'wavespeed-ai/infinitetalk'
RATE = 0.0633          # دولار للثانية (مقاس: 18 ث = 1.14 دولار بجودة 720p) — تقدير فقط
MAX_SECONDS = float(os.environ.get('MAX_SECONDS', 30))
MAX_TOTAL = float(os.environ.get('MAX_TOTAL', 3.0))
TIMEOUT = 40 * 60

def dur(p):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))

def call(method, url, key, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def raw_url(path):
    repo = os.environ['GITHUB_REPOSITORY']; sha = os.environ['GITHUB_SHA']
    return f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'

def main(name):
    key = os.environ.get('WAVESPEED_API_KEY')
    if not key: sys.exit('✗ المفتاح WAVESPEED_API_KEY غير موجود في أسرار GitHub')
    base = f'productions/{name}'; cfg = json.load(open(f'{base}/presenter.json', encoding='utf-8'))
    image = cfg['image']; res = cfg.get('resolution', '720p')
    if not os.path.exists(image): sys.exit(f'✗ الصورة غير موجودة: {image}')
    todo, total = [], 0.0
    for c in cfg['clips']:
        a, o = f"{base}/{c.get('audio') or c['right_audio']}", f"{base}/{c['output']}"
        if os.path.exists(o): print(f'↺ موجود، لن يُولَّد ولن يُدفع: {o}'); continue
        if not os.path.exists(a): sys.exit(f'✗ الصوت غير موجود: {a}')
        d = dur(a)
        if c.get('order') in ('left_right', 'right_left'): d += dur(f"{base}/{c['left_audio']}")  # الصوتان متتاليان فتُدفع مدتهما معًا
        if d > c.get('max_seconds', MAX_SECONDS): sys.exit(f'✗ {a} مدته {d:.1f} ث، أطول من الحد {MAX_SECONDS:.0f} ث. أُوقف كل شيء.')
        cost = math.ceil(d / 5) * 5 * RATE; total += cost; todo.append((a, o, d, cost, c))
        print(f'• {c.get("audio") or c["output"]}: {d:.1f} ث ← تقدير {cost:.2f} دولار')
    if not todo: print('لا شيء جديد للتوليد.'); return
    print(f'المجموع التقديري: {total:.2f} دولار (الحد {MAX_TOTAL:.2f})')
    if total > MAX_TOTAL: sys.exit('✗ التكلفة التقديرية أعلى من الحد. أُوقف كل شيء.')
    for a, o, d, cost, c in todo:
        if c.get('left_audio'):  # حوار بشخصين: صورة واحدة وصوتان متساويان في الطول (النموذج Multi)
            body = {'image': raw_url(c['image']), 'left_audio': raw_url(f"{base}/{c['left_audio']}"), 'right_audio': raw_url(a),
                    'order': c.get('order', 'meanwhile'), 'resolution': res, 'seed': -1}
            if c.get('prompt'): body['prompt'] = c['prompt']
            model = c.get('model', 'wavespeed-ai/infinitetalk/multi')
        else:
            body = {'image': raw_url(image), 'audio': raw_url(a), 'resolution': res, 'seed': -1}; model = MODEL
        try: r = call('POST', f'{API}/{model}', key, body)
        except urllib.error.HTTPError as e: sys.exit(f'✗ رُفض الطلب ({e.code}): {e.read().decode()[:500]}')
        pid = (r.get('data') or {}).get('id')
        if not pid: sys.exit(f'✗ لم يُرجع الطلب رقمًا: {r}')
        print(f'→ أُرسل {a} (رقم {pid})'); t0 = time.time()
        while True:
            time.sleep(10)
            st = call('GET', f'{API}/predictions/{pid}/result', key).get('data') or {}
            s = st.get('status')
            if s == 'completed': break
            if s in ('failed', 'cancelled', 'timeout', 'deleted'): sys.exit(f'✗ فشل التوليد ({s}): {st.get("error")}')
            if time.time() - t0 > TIMEOUT: sys.exit(f'✗ تجاوز المهلة. الرقم {pid} للمتابعة يدويًا.')
            print(f'  … {s} ({int(time.time()-t0)} ث)')
        url = (st.get('outputs') or [None])[0]
        if not url: sys.exit(f'✗ اكتمل بلا ملف: {st}')
        urllib.request.urlretrieve(url, o); od = dur(o)
        print(f'✓ {o}: {od:.1f} ث (الصوت {d:.1f} ث)')
        if od + 0.5 < d: sys.exit('✗ المقطع أقصر من الصوت. راجعه قبل استخدامه.')

if __name__ == '__main__':
    main(sys.argv[1])
