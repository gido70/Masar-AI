#!/usr/bin/env python3
"""الأصوات عبر WaveSpeed (ElevenLabs). التشغيل: python studio/make_voice.py <الإنتاج> [ملف الإعداد]
الإعداد الافتراضي productions/<الإنتاج>/voice.json:
  {"model": "elevenlabs/multilingual-v2", "voice_id": "George", "stability": 0.5, "similarity": 0.75,
   "use_speaker_boost": true, "clips": [{"text": "...", "output": "narration-open.mp3"}, ...]}
الضوابط: لا يولّد ملفًا موجودًا · حد للأحرف MAX_CHARS · المفتاح من البيئة فقط. السعر: 0.20$ لكل 1000 حرف.
"""
import json, os, sys, time, urllib.request, urllib.error
API = 'https://api.wavespeed.ai/api/v3'; MAX_CHARS = int(os.environ.get('MAX_CHARS', 6000))

def call(method, url, key, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e: sys.exit(f'✗ HTTP {e.code}: {e.read().decode()[:400]}')

def main(name, cfgname='voice.json'):
    key = os.environ.get('WAVESPEED_API_KEY') or sys.exit('✗ WAVESPEED_API_KEY غير موجود')
    base = f'productions/{name}'; cfg = json.load(open(f'{base}/{cfgname}', encoding='utf-8'))
    todo = [c for c in cfg['clips'] if not os.path.exists(f"{base}/{c['output']}")]
    chars = sum(len(c['text']) for c in todo)
    print(f'{len(todo)} مقطع، {chars} حرفًا ← تقدير {chars*0.0002:.3f} دولار (الحد {MAX_CHARS} حرف)')
    if chars > MAX_CHARS: sys.exit('✗ النص أطول من الحد.')
    for c in todo:
        body = {k: cfg[k] for k in ('voice_id', 'stability', 'similarity', 'use_speaker_boost') if k in cfg}; body['text'] = c['text']
        r = call('POST', f"{API}/{cfg['model']}", key, body); pid = (r.get('data') or {}).get('id') or sys.exit(f'✗ لا رقم: {r}')
        t0 = time.time()
        while True:
            time.sleep(2); st = call('GET', f'{API}/predictions/{pid}/result', key).get('data') or {}
            if st.get('status') == 'completed': break
            if st.get('status') in ('failed', 'cancelled', 'timeout', 'deleted'): sys.exit(f"✗ فشل: {st.get('error')}")
            if time.time() - t0 > 600: sys.exit('✗ تجاوز المهلة')
        urllib.request.urlretrieve((st.get('outputs') or [None])[0], f"{base}/{c['output']}"); print(f"✓ {c['output']}")

if __name__ == '__main__':
    main(*sys.argv[1:3])
