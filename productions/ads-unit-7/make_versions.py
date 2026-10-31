"""الوحدة 7: نسخ سَمَر الثلاث (فضول، تباين، تعاطف) بمقاسين، بالمونتاج من لقطات الوحدتين 5 و6 (0$)."""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
U5, U6 = '../ads-unit-5', '../ads-unit-6'
AD = f'{U6}/samar-ad.mp4'          # الإعلان الكامل (الوحدة 6)، ص6 يبدأ عند 23.3
CARD_BG = '2e1a0e'
FONT = '../../studio/fonts/Tajawal-Bold.ttf'
os.makedirs('tmp', exist_ok=True)

def sh(c): subprocess.run(c, shell=True, check=True)

def text_png(name, text, W, H, size, ypos):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT, size)
    lines = text.split('\n'); lh = int(size*1.35); pad = int(size*0.45); y0 = int(H*ypos)
    boxes = [d.textbbox((0, 0), l, font=f, direction='rtl', language='ar') for l in lines]
    tw = max(b[2]-b[0] for b in boxes); x0 = (W-tw)//2
    d.rounded_rectangle((x0-pad, y0-pad*0.7, x0+tw+pad, y0+lh*len(lines)+pad*0.3), radius=pad, fill=(0, 0, 0, 130))
    for i, (l, bb) in enumerate(zip(lines, boxes)):
        w = bb[2]-bb[0]; d.text(((W-w)//2-bb[0], y0+i*lh-bb[1]+int(size*0.1)), l, font=f, fill='white', direction='rtl', language='ar')
    img.save(f'tmp/{name}.png'); return f'tmp/{name}.png'

TX = {'cur': 'إلى أين يذهب هذا البخار؟', 'con1': 'وحدَنا…', 'con2': '…ومعًا',
      'emp': 'جاري منذ سنين… ولم نشرب فنجانًا معًا'}

# قص طولي: ('crop', cx) ثابت · ('pan', cx0, cx1) يتحرك · ('split', (xL,yL), (xR,yR)) · ('blur',)
def vfilter(fmt, mode, dur):
    if fmt == 'h': return 'scale=1920:1080'
    cw = 607
    if mode[0] == 'crop':
        return f'crop={cw}:1080:{int(mode[1]*1920-cw/2)}:0,scale=1080:1920'
    if mode[0] == 'pan':
        a, b = mode[1]*1920-cw/2, mode[2]*1920-cw/2
        return f"crop={cw}:1080:'{a:.0f}+({b-a:.0f})*t/{dur}':0,scale=1080:1920"
    if mode[0] == 'blur':
        return ('split[o][b];[b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:2,eq=brightness=-0.08[bg];'
                '[o]scale=1080:-2[fg];[bg][fg]overlay=0:(H-h)/2')
    if mode[0] == 'card':
        return 'crop=845:1080:537:0,scale=1080:-2,pad=1080:1920:0:(oh-ih)/2:color=0x%s' % CARD_BG
    if mode[0] == 'split':
        (xl, yl), (xr, yr) = mode[1], mode[2]; w, h = 900, 800
        return (f'split[l][r];[l]crop={w}:{h}:{xl-w//2}:{yl-h//2},scale=1080:960[t];'
                f'[r]crop={w}:{h}:{xr-w//2}:{yr-h//2},scale=1080:960[u];[t][u]vstack')

def seg(out, src, ss, to, fmt, mode, txt=None):
    dur = to-ss
    vf = f'[0:v]trim={ss}:{to},setpts=PTS-STARTPTS,fps=24,{vfilter(fmt, mode, dur)},setsar=1,format=yuv420p'
    inp = f'-i {src}'
    if txt:
        W, H = (1920, 1080) if fmt == 'h' else (1080, 1920)
        t = TX[txt] if fmt == 'h' else TX[txt].replace('… ', '…\n')
        png = text_png(f'{txt}-{fmt}', t, W, H, 78 if fmt == 'h' else 76, 0.79 if fmt == 'h' else 0.70)
        vf += f'[v0];[1:v]format=rgba,fade=t=in:d=0.25:alpha=1[tx];[v0][tx]overlay=0:0:shortest=1'
        inp += f' -loop 1 -t {dur} -i {png}'
    sh(f'ffmpeg -v error -y {inp} -filter_complex "{vf}" -an -c:v libx264 -preset ultrafast -crf 16 -t {dur} {out}')
    return out

# أوضاع القص الطولي لكل جزء من الإعلان (مخطط الإطارات، 31 أكتوبر)
V_AD = [(5.5, 9.5, ('crop', 0.47)), (9.5, 13.0, ('crop', 0.50)), (13.0, 16.5, ('pan', 0.14, 0.30)),
        (16.5, 18.8, ('pan', 0.30, 0.52)), (18.8, 23.3, ('crop', 0.83)), (23.3, 28.0, ('blur',)), (28.0, 32.0, ('card',))]
def ad_parts(a, b, fmt):
    """أجزاء الإعلان من a إلى b، كل جزء بقصه الطولي."""
    out = []
    for s, e, m in V_AD:
        s2, e2 = max(s, a), min(e, b)
        if fmt == 'h' and m[0] == 'card': m = ('blur',)
        if e2 - s2 > 0.01: out.append((AD, s2, e2, m, None))
    return out

BR, S1, S5, S6 = f'{U5}/samar-s4-bridge-v3.mp4', f'{U5}/samar-s1.mp4', f'{U5}/samar-s5.mp4', f'{U5}/samar-s6.mp4'
SPLIT = ('split', (520, 490), (1344, 490))
def plan(v, fmt):
    if v == 'curiosity':   # البخار سؤالًا، ثم نهايته جوابًا
        return [(BR, 0.0, 3.5, ('pan', 0.12, 0.26), 'cur')] + ad_parts(5.5, 13.0, fmt) + ad_parts(16.5, 32.0, fmt)
    if v == 'contrast':    # وحدنا… ثم معًا
        return [(S1, 0.3, 2.1, SPLIT, 'con1'), (S6, 1.0, 2.7, ('blur',), 'con2')] + ad_parts(5.5, 32.0, fmt)
    if v == 'empathy':     # الجار وحده (البصيرة)، ثم يلتفت ويبتسم لاحقًا
        return ([(S5, 0.3, 3.5, ('crop', 0.80), 'emp')] + ad_parts(5.5, 18.8, fmt)
                + [(S5, 3.5, 6.7, ('crop', 0.83), None)] + ad_parts(23.3, 32.0, fmt))

def build(v, fmt):
    parts, t, marks = [], 0.0, {}
    for i, (src, a, b, m, txt) in enumerate(plan(v, fmt)):
        if src == AD and a <= 5.5 < b: marks['pour'] = t + (5.5 - a)
        if src == AD and a <= 25.0 < b: marks['vo'] = t + (25.0 - a)
        parts.append(seg(f'tmp/{v}-{fmt}-{i}.mp4', src, a, b, fmt, m, txt)); t += b - a
    with open(f'tmp/list-{v}-{fmt}.txt', 'w') as f:
        f.writelines(f"file '{os.path.basename(p)}'\n" for p in parts)
    sh(f'cd tmp && ffmpeg -v error -y -f concat -safe 0 -i list-{v}-{fmt}.txt -c copy {v}-{fmt}-video.mp4')
    T, vo, pour = t, marks['vo'], marks['pour']
    # الصوت يُبنى من جديد: موسيقى متصلة، وجو الحي، وصب القهوة عند ص2، وجملة المعلّق كاملة ثم ثانية صمت تقريبًا قبل النهاية
    af = (f"[1:a]atrim=0:{T},asetpts=PTS-STARTPTS,afade=t=in:d=0.8,afade=t=out:st={T-1.6}:d=1.6,"
          f"volume='if(between(t,{vo-0.4:.2f},{vo+2.4:.2f}),0.16,0.42)':eval=frame[m];"
          f"[2:a]loudnorm=I=-16:TP=-1.5,adelay={int(vo*1000)}|{int(vo*1000)}[vo];"
          f"[3:a]atrim=0.29:3.79,asetpts=PTS-STARTPTS,volume=0.35,afade=t=in:d=0.3,afade=t=out:st=2.8:d=0.7[amb];"
          f"[4:a]atrim=0.29:4.29,asetpts=PTS-STARTPTS,volume=1.6,afade=t=in:d=0.2,afade=t=out:st=3.5:d=0.5,"
          f"adelay={int(pour*1000)}|{int(pour*1000)}[pour];"
          f"[m][vo][amb][pour]amix=inputs=4:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5[au]")
    if fmt == 'h': vfade = f'fade=t=in:d=0.4'
    else: vfade = f'fade=t=in:d=0.4'
    out = f'samar-{v}-{"16x9" if fmt == "h" else "9x16"}.mp4'
    sh(f'ffmpeg -v error -y -i tmp/{v}-{fmt}-video.mp4 -i ../ads-unit-0/music-C-emotional.mp3 -i {U6}/samar-vo.mp3 '
       f'-i {S1} -i {U5}/samar-s2.mp4 -filter_complex "[0:v]{vfade}[v];{af}" -map "[v]" -map "[au]" '
       f'-c:v libx264 -preset fast -crf 20 -c:a aac -b:a 160k -t {T} {out}')
    print(out, round(T, 2), 'vo at', round(vo, 2), 'ends', round(vo + 2.04, 2))

if __name__ == '__main__':
    import sys
    vs = sys.argv[1:2] or ['curiosity', 'contrast', 'empathy']
    fs = sys.argv[2:3] or ['h', 'v']
    for v in vs:
        for fmt in fs: build(v, fmt)
