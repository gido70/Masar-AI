#!/usr/bin/env python3
"""الصورة المصغرة ليوتيوب بقالب مسار الثابت (1280×720).
الخطوط ثابتة لكل الوحدات: العنوان بالأميري العريض (Amiri-Bold)، والشارة والسطر الفرعي بتجوال العريض.
التشغيل: python studio/make_thumbnail.py <صورة المقدّم> <رقم الوحدة> "<السطر الأول>" "<السطر الثاني بالأحمر>" "<السطر الفرعي>" <ملف الناتج.jpg> [قص_يسار]
"""
import os, sys, tempfile
from PIL import Image
R = os.path.dirname(os.path.abspath(__file__))
def main(photo, n, l1, l2, sub, out, crop_x='40'):
    cx = int(crop_x); d = tempfile.mkdtemp()
    fs = min(138, int(138 * 7.5 / max(len(l1), len(l2), 1)))  # سطر واحد لكل جزء، يصغر الخط مع الطول
    im = Image.open(photo).convert('RGB'); s = 720 / im.height; im = im.resize((int(im.width * s), 720))
    im.crop((cx, 0, cx + 720, 720)).save(f'{d}/p.png')
    html = f'''<html dir="rtl"><head><style>
@font-face{{font-family:A;src:url(file://{R}/fonts/Amiri-Bold.ttf)}}
@font-face{{font-family:T;src:url(file://{R}/fonts/Tajawal-Bold.ttf)}}
body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#fff;position:relative}}
.ph{{position:absolute;left:0;top:0;width:720px;height:720px;background:url(p.png) center/cover}}
.fade{{position:absolute;left:470px;top:0;width:260px;height:720px;background:linear-gradient(to right,rgba(255,255,255,0),#fff 85%)}}
.tx{{position:absolute;right:70px;top:0;width:540px;height:720px;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding-bottom:40px}}
.b{{font-family:T;background:#D62828;color:#fff;font-size:36px;padding:8px 26px 4px;border-radius:12px}}
.h{{font-family:A;font-size:{fs}px;white-space:nowrap;line-height:1.12;color:#1B1B2F;margin-top:6px}}
.h span{{color:#D62828}}
.ln{{width:100%;height:5px;background:#D62828;margin:18px 0 18px}}
.s{{font-family:T;font-size:44px;color:#1B1B2F}}
.logo{{position:absolute;right:70px;bottom:40px;height:62px}}
</style></head><body><div class="ph"></div><div class="fade"></div>
<div class="tx"><div class="b">الوحدة {n}</div><div class="h">{l1}<br><span>{l2}</span></div><div class="ln"></div><div class="s">{sub}</div></div>
<img class="logo" src="file://{R}/assets/logo.png"></body></html>'''
    open(f'{d}/t.html', 'w', encoding='utf-8').write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 720})
        pg.goto(f'file://{d}/t.html'); pg.wait_for_timeout(800); pg.screenshot(path=f'{d}/t.png'); b.close()
    Image.open(f'{d}/t.png').convert('RGB').save(out, quality=92); print('✓', out)
if __name__ == '__main__':
    main(*sys.argv[1:])
