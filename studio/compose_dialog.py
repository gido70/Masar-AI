#!/usr/bin/env python3
"""حوار بشخصين بلا Multi: وجه المتكلم وحده يُؤخذ من مقطعه المنفرد ويُركَّب على الصورة المشتركة.

الاستخدام: python studio/compose_dialog.py productions/<n>/dialog.json
dialog.json: {"base": "two-shot-b.png",
  "speakers": {"woman": {"video": "talk-woman.mp4", "crop": [x0,y0,x1,y1], "face": [cx,cy,rx,ry]}, ...},
  "turns": [{"speaker": "woman", "start": 0.0, "dur": 4.48, "output": "dialog-q1.mp4"}, ...]}
crop: موضع الصورة المقصوصة التي حُرّكت داخل الصورة المشتركة · face: قطع ناقص حول الوجه (إحداثيات الصورة المشتركة).
الصامت يبقى من الصورة المشتركة نفسها، ففمه مغلق دائمًا.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter

def main(path):
    cfg = json.load(open(path, encoding='utf-8')); base = os.path.dirname(os.path.abspath(path))
    P = lambda x: os.path.join(base, x)
    for name, sp in cfg['speakers'].items():
        x0, y0, x1, y1 = sp['crop']; cx, cy, rx, ry = sp['face']; w, h = x1 - x0, y1 - y0
        m = Image.new('L', (w, h), 0)
        ImageDraw.Draw(m).ellipse((cx - x0 - rx, cy - y0 - ry, cx - x0 + rx, cy - y0 + ry), fill=255)
        m.filter(ImageFilter.GaussianBlur(sp.get('feather', 14))).save(P(f'_mask-{name}.png'))
    for t in cfg['turns']:
        sp = cfg['speakers'][t['speaker']]; x0, y0, x1, y1 = sp['crop']; w, h = x1 - x0, y1 - y0
        fc = (f"[1:v]trim=start={t['start']:.3f}:duration={t['dur']:.3f},setpts=PTS-STARTPTS,scale={w}:{h},format=rgba[sp];"
              f"[2:v]format=gray,scale={w}:{h}[mk];[sp][mk]alphamerge[fg];"
              f"[0:v]scale=1280:720,format=rgba[bg];[bg][fg]overlay={x0}:{y0}:shortest=1,fps=25,format=yuv420p[v]")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '25', '-i', P(cfg['base']),
                        '-i', P(sp['video']), '-loop', '1', '-i', P(f'_mask-{t["speaker"]}.png'),
                        '-filter_complex', fc, '-map', '[v]', '-t', f"{t['dur']:.3f}", '-an',
                        '-c:v', 'libx264', '-crf', '16', P(t['output'])], check=True)
        print('✓', t['output'], t['dur'])

if __name__ == '__main__':
    main(sys.argv[1])
