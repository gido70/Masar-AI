#!/usr/bin/env python3
"""مصنع فيديو مسار — ينتج فيديو كاملًا من ملف وصف (spec.json).

الاستخدام:
    python studio/make_video.py productions/<name>/spec.json

المتطلبات: ffmpeg، و pip install -r studio/requirements.txt، ثم: python -m playwright install chromium
"""
import json, os, re, subprocess, sys, shutil
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, 'fonts')
ASSETS = os.path.join(HERE, 'assets')

# ---------------------------------------------------------------- الهوية
THEMES = {
    "video": dict(INK='#1A1B22', ACC='#D62828', SEC='#9A5B00', BG='#FFFFFF', PAPER='#FFF7E8',
                  MUT='#5A5F6B', FILM='#ECE8E1', LINE='#D9D3C7', GRN='#1E7B4F', motif='film'),
}

def run(cmd):
    subprocess.run(cmd, check=True)

def ff(*args):
    run(['ffmpeg', '-v', 'error', '-y', *args])

def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                          '-of', 'csv=p=0', path]).decode().strip())

# ---------------------------------------------------------------- الصوت
def normalize(src, out):
    ff('-i', src, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-b:a', '192k', out)

def trim_silence(src, out):
    ff('-i', src, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
       'silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5:LRA=11',
       '-ar', '44100', '-b:a', '192k', out)

def silences(src, db=-35, d=0.3):
    err = subprocess.run(['ffmpeg', '-nostats', '-i', src, '-af', f'silencedetect=n={db}dB:d={d}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]
    e = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    return list(zip(s, e))

# ---------------------------------------------------------------- البطاقات (HTML)
def css(T, w, h):
    return f'''@font-face{{font-family:Amiri;src:url(file://{FONTS}/Amiri-Regular.ttf);font-weight:400}}
@font-face{{font-family:Amiri;src:url(file://{FONTS}/Amiri-Bold.ttf);font-weight:700}}
@font-face{{font-family:Tajawal;src:url(file://{FONTS}/Tajawal-Bold.ttf);font-weight:700}}
*{{box-sizing:border-box}} body{{margin:0;width:{w}px;height:{h}px;background:{T['BG']};color:{T['INK']};font-family:Amiri;direction:rtl;position:relative;overflow:hidden}}
.strip{{position:absolute;left:0;right:0;height:40px;background:{T['FILM']};display:flex;gap:26px;align-items:center;padding:0 30px}}
.strip i{{display:block;width:32px;height:20px;border-radius:5px;background:{T['BG']}}}
.rec{{display:flex;align-items:center;gap:14px;font-family:Tajawal;font-size:32px;color:{T['MUT']}}} .rec b{{width:24px;height:24px;border-radius:50%;background:{T['ACC']}}}
h1{{margin:0;font-size:100px;font-weight:700;line-height:1.15}} h1 em{{font-style:normal;color:{T['ACC']}}}'''

def em(text, T):
    """[[كلمة]] تُلوَّن بلون التأكيد."""
    return re.sub(r'\[\[(.+?)\]\]', lambda m: f'<em style="font-style:normal;color:{T["ACC"]}">{m.group(1)}</em>', text)

def frame(T, label, scene, body):
    st = ''.join('<i></i>' for _ in range(40))
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{css(T,1920,1080)}</style></head><body>
<div class="strip" style="top:0">{st}</div><div class="strip" style="bottom:0">{st}</div>
<div class="rec" style="position:absolute;top:78px;right:110px"><b></b>{label}</div>
<img src="file://{ASSETS}/logo.png" style="position:absolute;top:62px;left:100px;height:84px">
<div style="position:absolute;bottom:58px;left:110px;font-family:Tajawal;font-size:26px;color:{T['MUT']}">{scene}</div>
{body}</body></html>'''

def card_html(c, T, label, scene):
    k = c['kind']; title = f'<h1 style="position:absolute;top:150px;right:110px">{em(c["title"], T)}</h1>'
    if k == 'grid':
        items = ''.join(f'''<div class="rv" style="background:{T['PAPER']};border:3px solid {T['LINE']};border-radius:24px;padding:22px 24px;min-height:200px">
<div style="width:64px;height:64px;border-radius:50%;background:{T['ACC']};color:#fff;font-family:Tajawal;font-size:36px;display:flex;align-items:center;justify-content:center">{i+1}</div>
<div style="font-size:50px;font-weight:700;margin-top:10px">{it[0]}</div><div style="font-size:34px;color:{T['MUT']}">{it[1] if len(it)>1 else ''}</div></div>''' for i, it in enumerate(c['items']))
        body = title + f'<div style="position:absolute;top:350px;right:110px;left:110px;display:grid;grid-template-columns:repeat({c.get("cols",4)},1fr);gap:22px">{items}</div>'
    elif k == 'tree':
        rows = ''.join(f'''<div class="rv" style="display:flex;align-items:center;gap:26px;margin-bottom:18px"><div style="width:340px;font-size:52px;font-weight:700;background:{T['PAPER']};border:3px solid {T['LINE']};border-radius:20px;padding:8px 28px">{a}</div>
<div style="flex:none;width:80px;height:6px;background:{T['ACC']};border-radius:3px"></div><div style="font-size:52px;color:{T['SEC']};font-weight:700">{b}</div></div>''' for a, b in c['rows'])
        side = f'<div class="rv" style="position:absolute;top:360px;left:110px;width:430px;background:{T["PAPER"]};border:3px dashed {T["LINE"]};border-radius:24px;padding:24px 30px;font-size:40px;line-height:1.4">{em(c["note"],T)}</div>' if c.get('note') else ''
        body = title + f'<div style="position:absolute;top:340px;right:110px">{rows}</div>' + side
    elif k == 'rule_bars':
        r = c['rule']
        banner = f'''<div class="rv" style="position:absolute;top:330px;right:110px;width:1700px;background:{T['ACC']};color:#fff;border-radius:30px;padding:30px 44px;display:flex;align-items:center;gap:40px">
<div style="font-size:120px;font-weight:700;font-family:Tajawal">{r['big']}</div><div style="font-size:56px;line-height:1.3">{r['text']}</div>
<div style="margin-right:auto;font-size:34px;line-height:1.4">{r.get('note','')}</div></div>'''
        bars = ''.join(f'''<div class="rv" style="display:flex;align-items:center;gap:24px;margin-bottom:16px"><div style="width:300px;font-size:44px;font-weight:700">{a}</div>
<div style="height:46px;width:{int(1000*w)}px;background:{T['SEC']};border-radius:12px"></div><div style="font-size:42px;color:{T['SEC']};font-weight:700">{b}</div></div>''' for a, b, w in c['bars'])
        body = title + banner + f'<div style="position:absolute;top:640px;right:110px;left:110px">{bars}</div>'
    elif k == 'cards':
        colors = {'green': T['GRN'], 'amber': T['SEC'], 'red': T['ACC']}
        items = ''.join(f'''<div class="rv" style="border:4px solid {colors.get(it[2],T['SEC'])};border-radius:26px;padding:24px;background:#fff;min-height:250px">
<div style="font-size:42px;font-weight:700;line-height:1.3">{it[0]}</div><div style="margin-top:14px;font-size:48px;font-weight:700;color:{colors.get(it[2],T['SEC'])}">{it[1]}</div></div>''' for it in c['items'])
        warn = f'<div class="rv" style="position:absolute;bottom:120px;right:110px;left:110px;background:{T["PAPER"]};border-radius:24px;padding:22px 34px;font-size:46px">{em(c["warning"],T)}</div>' if c.get('warning') else ''
        body = title + f'<div style="position:absolute;top:340px;right:110px;left:110px;display:grid;grid-template-columns:repeat({len(c["items"])},1fr);gap:22px">{items}</div>' + warn
    elif k == 'end':
        st = ''.join('<i></i>' for _ in range(40))
        return f'''<!doctype html><html><head><meta charset="utf-8"><style>{css(T,1920,1080)}</style></head><body>
<div class="strip" style="top:0">{st}</div><div class="strip" style="bottom:0">{st}</div>
<img src="file://{ASSETS}/logo.png" style="position:absolute;top:200px;left:50%;transform:translateX(-50%);height:330px">
<div style="position:absolute;top:600px;width:100%;text-align:center;font-size:96px;font-weight:700">{em(c['title'],T)}</div>
<div style="position:absolute;top:760px;width:100%;text-align:center;font-family:Tajawal;font-size:44px;color:{T['MUT']}">{c.get('sub','')}</div></body></html>'''
    else:
        raise ValueError('نوع بطاقة غير معروف: ' + k)
    return frame(T, label, scene, body)

def screen_html(s, T):
    """محتوى شاشة المقدّم (1080×750)."""
    lines = ''.join(f'<div class="rv" style="font-size:62px;line-height:1.45;font-weight:700">{x}</div>' for x in s.get('lines', []))
    btn = f'<div class="rv" style="margin-top:26px;display:inline-block;background:{T["ACC"]};color:#fff;border-radius:22px;padding:14px 34px;font-size:54px;font-weight:700">{s["button"]}</div>' if s.get('button') else ''
    foot = f'<div class="rv" style="margin-top:16px;font-size:40px;color:{T["MUT"]}">{s["foot"]}</div>' if s.get('foot') else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{css(T,1080,750)}</style></head><body><div style="position:absolute;top:44px;right:64px;left:64px">
<div class="rec"><b></b>{s.get('kicker','')}</div>
<div style="font-size:92px;font-weight:700;line-height:1.15;margin-top:18px">{em(s['title'],T)}</div>{lines}{btn}{foot}</div></body></html>'''

def render_states(pg, html, out_prefix, w=1920, h=1080):
    """يرسم البطاقة بكل حالات الظهور التدريجي. يعيد قائمة الصور."""
    n = html.count('class="rv"'); files = []
    pg.set_viewport_size({'width': w, 'height': h})
    for i in range(n + 1):
        hh = html.replace('</body>', f'<script>document.querySelectorAll(".rv").forEach((e,j)=>{{if(j>={i})e.style.visibility="hidden"}})</script></body>') if n else html
        p = f'{out_prefix}.html'; open(p, 'w', encoding='utf-8').write(hh)
        pg.goto('file://' + os.path.abspath(p)); pg.wait_for_timeout(250)
        f = f'{out_prefix}_r{i}.png'; pg.screenshot(path=f); files.append(f)
        if not n: break
    return files

# ---------------------------------------------------------------- تركيب الشاشة على المقدّم
def composite_screen(src, states, reveal, out, work, fps=25):
    """يركّب محتوى الشاشة على فيديو المقدّم. states: صور حالات الظهور، reveal: توقيت ظهور كل عنصر."""
    fr = os.path.join(work, 'fr'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
    ff('-i', src, '-vf', f'fps={fps}', os.path.join(fr, '%04d.png'))
    contents = [Image.open(x).convert('RGB') for x in states]; bbox = None; cache = {}
    files = sorted(os.listdir(fr))
    for i, f in enumerate(files):
        tt = i / fps; k = sum(1 for r in reveal if tt >= r) if len(states) > 1 else 0
        content = contents[min(k, len(contents) - 1)]
        a = np.asarray(Image.open(os.path.join(fr, f)).convert('RGB')).astype(float)
        H, W, _ = a.shape; X0 = int(W * 0.40)
        reg = a[:, X0:]; m = (reg.mean(-1) > 200) & ((reg.max(-1) - reg.min(-1)) < 38)
        if bbox is None or i % 10 == 0:
            cols = np.where(m.sum(0) > H * 0.35)[0]; rows = np.where(m.sum(1) > (W - X0) * 0.35)[0]
            if len(cols) and len(rows): bbox = (X0 + cols.min(), rows.min(), X0 + cols.max() + 1, rows.max() + 1)
        x0, y0, x1, y1 = bbox; pad = int((y1 - y0) * 0.04)
        cw, ch = x1 - x0 - 2 * pad, y1 - y0 - 2 * pad; r = min(cw / content.width, ch / content.height)
        key = (id(content), int(content.width * r), int(content.height * r))
        if key not in cache: cache[key] = content.resize(key[1:], Image.LANCZOS)
        c = cache[key]
        layer = Image.new('RGB', (W, H), (255, 255, 255)); layer.paste(c, (x1 - pad - c.width, y0 + pad))
        full = np.zeros((H, W), bool); full[:, X0:] = m
        box = np.zeros((H, W), bool); box[y0:y1, x0:x1] = True
        mm = np.asarray(Image.fromarray(((full & box) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))).astype(float) / 255
        o = a * (1 - mm[..., None]) + np.asarray(layer).astype(float) * mm[..., None]
        Image.fromarray(o.clip(0, 255).astype('uint8')).save(os.path.join(fr, f))
    ff('-framerate', str(fps), '-i', os.path.join(fr, '%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', out)

# ---------------------------------------------------------------- الترجمة النصية
def ass(captions, path):
    def ts(t): return f'0:{int(t//60):02d}:{t%60:05.2f}'
    head = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Amiri,124,&H00FFFFFF,&H00FFFFFF,&H40221B1A,&H40221B1A,1,0,0,0,100,100,0,0,3,8,0,2,100,100,40,-1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    open(path, 'w', encoding='utf-8').write(head + ''.join(f'Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{t}\n' for a, b, t in captions))

# ---------------------------------------------------------------- فحص الإيقاع
MIN_ITEM, HOLD = 2.0, 1.0

def check_rhythm(name, reveal, n, d, hold):
    """قواعد الإيقاع: عنصر لكل توقيت، ثانيتان على الأقل لكل عنصر، وثبات قبل الانتقال."""
    errs = []
    if len(reveal) != n: errs.append(f'عدد reveal_at = {len(reveal)} وعدد العناصر = {n}')
    for k in range(1, len(reveal)):
        if reveal[k] - reveal[k-1] < MIN_ITEM - 1e-6: errs.append(f'العنصر {k} ظاهر {reveal[k]-reveal[k-1]:.2f} ث فقط')
    if reveal and d - reveal[-1] < MIN_ITEM + hold - 1e-6: errs.append(f'العنصر الأخير ظاهر {d-reveal[-1]:.2f} ث قبل الانتقال (المطلوب {MIN_ITEM+hold:.1f})')
    if reveal and (reveal[0] < 0 or reveal[-1] > d): errs.append('توقيت خارج مدة المشهد')
    for e in errs: print(f'⚠ {name}: {e}', flush=True)
    return errs

# ---------------------------------------------------------------- التجميع
def main(spec_path):
    import hashlib
    spec = json.load(open(spec_path, encoding='utf-8')); base = os.path.dirname(os.path.abspath(spec_path))
    T = THEMES[spec.get('theme', 'video')]; work = os.path.join(base, '_work'); os.makedirs(work, exist_ok=True)
    P = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
    label = spec['label']; segs = spec['segments']; N = len([s for s in segs if s['type'] != 'end'])
    strict = not os.environ.get('NO_STRICT')

    # 1) مدة كل مشهد، والصوت الخاص به (الصوت جزء من المشهد فيبقى التزامن مضمونًا)
    plan, problems = [], []
    for i, s in enumerate(segs):
        au = s.get('audio')
        if s['type'] == 'presenter':
            d = dur(P(s['video']))
            if au:
                alen = dur(P(au['file'])) - au.get('start', 0) if 'end' not in au else au['end'] - au.get('start', 0)
                if alen > d + 0.15: problems.append(f'المشهد {i+1}: الصوت ({alen:.2f} ث) أطول من فيديو المقدّم ({d:.2f} ث) فسيُقطع'); print('⚠', problems[-1])
        elif s['type'] == 'card' and au:
            alen = au['end'] - au['start']; d = alen + s.get('hold', HOLD)
        else:
            d = s.get('duration', 3.0)
        plan.append(d)
        if s['type'] == 'card':
            n = card_html(s['card'], T, label, '').count('class="rv"')
            problems += check_rhythm(f'المشهد {i+1}', s['card'].get('reveal_at', []), n, d, s.get('hold', HOLD))
        if s['type'] == 'presenter' and 'reveal_at' in s.get('screen', {}):
            n = screen_html(s['screen'], T).count('class="rv"'); rv = s['screen']['reveal_at']
            if len(rv) != n: problems.append(f'المشهد {i+1}: عدد reveal_at = {len(rv)} وعدد العناصر = {n}'); print('⚠', problems[-1])
    if problems and strict: sys.exit('✗ أوقفت الإنتاج: قواعد الإيقاع غير متحققة (للتجاوز: NO_STRICT=1)')

    # 2) المشاهد
    from playwright.sync_api import sync_playwright
    clips, caps, t = [], [], 0.0
    with sync_playwright() as p:
        pg = p.chromium.launch().new_page()
        for i, s in enumerate(segs):
            d = plan[i]; scene = f'المشهد {i+1} من {N}'
            h = hashlib.md5(json.dumps([{k: v for k, v in s.items() if k != 'captions'}, label, d], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:8]
            out = os.path.join(work, f'seg{i}_{h}.mp4')
            for a, b, txt in s.get('captions', []): caps.append((t + a, t + b, txt))
            if os.path.exists(out) and os.path.getsize(out) > 1000 and not os.environ.get('FORCE'):
                clips.append((out, t, t + d)); t += d; print('↺ موجود:', out, flush=True); continue
            if s['type'] == 'presenter':
                scr = os.path.join(work, f'scr{i}'); states = render_states(pg, screen_html(s['screen'], T), scr, 1080, 750)
                composite_screen(P(s['video']), states, s['screen'].get('reveal_at', [0] * (len(states) - 1)), out, work)
            elif s['type'] == 'card':
                states = render_states(pg, card_html(s['card'], T, label, scene), os.path.join(work, f'card{i}'))
                n = len(states) - 1; lst = os.path.join(work, f'card{i}.txt')
                rv = s['card'].get('reveal_at') or [0.5 + k * (d - 1.6) / max(n, 1) for k in range(n)]
                marks = [0.0] + list(rv) + [d]
                with open(lst, 'w') as f:
                    for k in range(n + 1):
                        f.write(f"file '{states[k]}'\nduration {max(marks[k+1]-marks[k], 0.04):.3f}\n")
                    f.write(f"file '{states[-1]}'\n")
                ff('-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=25,scale=1920:1080,format=yuv420p', '-c:v', 'libx264', '-crf', '18', out)
            elif s['type'] == 'end':
                img = render_states(pg, card_html(dict(kind='end', **s), T, label, ''), os.path.join(work, 'end'))[0]
                ff('-loop', '1', '-framerate', '25', '-t', str(d + 0.5), '-i', img, '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '18', out)
            clips.append((out, t, t + d)); t += d; print('✓ مشهد', i + 1, f'({d:.2f} ث)', flush=True)

    # 3) الصوت: لكل مشهد مقطعه، مُكمَّل بصمت حتى نهاية المشهد
    END = t; a_in, a_fl, a_lab = [], [], []
    seg_audio = any(s.get('audio') for s in segs)
    if seg_audio:
        for i, s in enumerate(segs):
            k = len(clips) + len(a_in) // 2; au = s.get('audio')
            if au:
                a_in += ['-i', P(au['file'])]
                tr = f"atrim={au.get('start',0)}:{au['end']}," if 'end' in au else (f"atrim=start={au['start']}," if 'start' in au else '')
                a_fl.append(f"[{k}:a]{tr}asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono,apad=whole_dur={plan[i]:.3f},atrim=0:{plan[i]:.3f}[s{i}]")
            else:
                a_fl.append(f"anullsrc=r=44100:cl=mono,atrim=0:{plan[i]:.3f}[s{i}]")
            a_lab.append(f'[s{i}]')
        a_fl.append(''.join(a_lab) + f"concat=n={len(segs)}:v=0:a=1,afade=t=out:st={END-1}:d=1[aout]")
    else:  # الطريقة القديمة: أجزاء متتالية على مستوى الملف
        for k, part in enumerate(spec['audio']):
            a_in += ['-i', P(part['file'])]
            a_fl.append(f"[{len(clips)+k}:a]atrim={part.get('start',0)}:{part.get('end',99999)},asetpts=PTS-STARTPTS[a{k}]")
        a_fl.append(''.join(f'[a{k}]' for k in range(len(spec['audio']))) + f"concat=n={len(spec['audio'])}:v=0:a=1,apad=whole_dur={END},afade=t=out:st={END-1}:d=1,atrim=0:{END}[aout]")

    # 4) الصورة: انتقالات ناعمة بلا إزاحة للتوقيت
    xd = spec.get('crossfade', 0.4); v_in, v_fl = [], []
    for k, (c, a, b) in enumerate(clips):
        pre = 0 if k == 0 else xd / 2; post = 0 if k == len(clips) - 1 else xd / 2; L = (b - a) + pre + post
        v_in += ['-i', c]
        v_fl.append(f"[{k}:v]scale=1920:1080:flags=lanczos,fps=25,setsar=1,format=yuv420p,tpad=start_mode=clone:start_duration={pre:.3f}:stop_mode=clone:stop_duration=2,trim=duration={L:.3f},setpts=PTS-STARTPTS[v{k}]")
    prev = 'v0'
    for k in range(1, len(clips)):
        v_fl.append(f"[{prev}][v{k}]xfade=transition=fade:duration={xd}:offset={clips[k][1]-xd/2:.3f}[x{k}]"); prev = f'x{k}'
    cap = os.path.join(work, 'cap.ass'); ass(caps, cap); v_fl.append(f"[{prev}]ass={cap},format=yuv420p[vout]")
    out = P(spec.get('output', 'output.mp4'))
    # yuv420p + High: يعمل على الهواتف والمتصفحات (yuv444p لا يعمل عليها)
    ff(*v_in, *a_in, '-filter_complex', ';'.join(v_fl + a_fl), '-map', '[vout]', '-map', '[aout]',
       '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.1',
       '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-movflags', '+faststart', '-t', f'{END:.3f}', out)
    print(f'✓ {out}  ({END:.1f} ثانية)')
    tl = [dict(scene=i+1, type=s['type'], start=round(c[1],2), end=round(c[2],2),
               reveal=[round(c[1]+r,2) for r in (s.get('card',{}).get('reveal_at') or s.get('screen',{}).get('reveal_at') or [])])
          for i, (s, c) in enumerate(zip(segs, clips))]
    json.dump(tl, open(os.path.join(work, 'timeline.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main(sys.argv[1])
