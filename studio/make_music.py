"""مولّد موسيقى الهوية (WaveSpeed · MiniMax Music · مدفوع).
يقرأ productions/<name>/music.json: قائمة tracks فيها id وprompt. كل مقطوعة آلية بلا كلمات.
حد تكلفة MAX_TOTAL · المفتاح من متغير البيئة WAVESPEED_API_KEY فقط."""
import json, os, subprocess, sys, time, urllib.request, urllib.error
API = 'https://api.wavespeed.ai/api/v3'
MAX_TOTAL = float(os.environ.get('MAX_TOTAL', 1.0)); TIMEOUT = 900

def die(m): print(m); sys.exit(1)
def call(method, url, key, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode())
def dur(p):
    return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip() or 0)

def main(name):
    key = os.environ.get('WAVESPEED_API_KEY') or die('✗ لا مفتاح WAVESPEED_API_KEY')
    base = f'productions/{name}'; cfg = json.load(open(f'{base}/music.json', encoding='utf-8'))
    model = cfg.get('model', 'minimax/music-2.6'); price = float(cfg.get('price_per_track', 0.15))
    todo = [t for t in cfg['tracks'] if not os.path.exists(f"{base}/music-{t['id']}.mp3")]
    total = price * len(todo)
    print(f'المقطوعات: {len(todo)} · التقديري {total:.2f}$ (الحد {MAX_TOTAL:.2f}$)')
    if total > MAX_TOTAL: die('✗ التكلفة التقديرية أعلى من الحد. أُوقف كل شيء.')
    for t in todo:
        body = {'prompt': t['prompt'], 'lyrics': '', 'is_instrumental': True}
        try: r = call('POST', f'{API}/{model}', key, body)
        except urllib.error.HTTPError as e: die(f'✗ رُفض الطلب ({e.code}): {e.read().decode()[:500]}')
        pid = (r.get('data') or {}).get('id') or die(f'✗ لا رقم: {r}')
        print(f"→ {t['id']} (رقم {pid})"); t0 = time.time()
        while True:
            time.sleep(8)
            st = call('GET', f'{API}/predictions/{pid}/result', key).get('data') or {}
            s = st.get('status')
            if s == 'completed': break
            if s in ('failed','cancelled','timeout','deleted'): die(f'✗ فشل ({s}): {st.get("error")}')
            if time.time()-t0 > TIMEOUT: die(f'✗ تجاوز المهلة، الرقم {pid}')
        url = (st.get('outputs') or [None])[0] or die(f'✗ بلا ملف: {st}')
        raw = f"{base}/music-{t['id']}.raw"; urllib.request.urlretrieve(url, raw)
        out = f"{base}/music-{t['id']}.mp3"
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',raw,'-ac','2','-ar','44100','-b:a','192k',out], check=True); os.remove(raw)
        print(f'✓ {out}: {dur(out):.1f} ث')

if __name__ == '__main__': main(sys.argv[1])
