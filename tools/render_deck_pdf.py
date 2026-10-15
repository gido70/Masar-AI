"""يرسم شرائح عرض (project/slides/*.html من أداة الشرائح) إلى PDF، وملاحظات المتحدث إلى Markdown.
التشغيل: python3 tools/render_deck_pdf.py <مجلد project> <خريطة صور json> <ملف PDF الناتج> <ملف الملاحظات>"""
import json, sys, os, re, html
from playwright.sync_api import sync_playwright
proj, imgmap, out_pdf, out_notes = sys.argv[1:5]
deck = json.load(open(os.path.join(proj, 'deck.json'), encoding='utf-8'))
m = json.load(open(imgmap, encoding='utf-8'))
font = os.path.abspath('assets/fonts')
pages, notes = [], []
for i, sid in enumerate(deck['order'], 1):
    s = open(os.path.join(proj, 'slides', sid + '.html'), encoding='utf-8').read()
    note = re.search(r'<aside>(.*?)</aside>', s, re.S)
    notes.append(f'## الشريحة {i}\n\n' + (html.unescape(note.group(1)).strip() if note else '') + '\n')
    s = re.sub(r'<aside>.*?</aside>', '', s, flags=re.S)
    for k, v in m.items(): s = s.replace(k, 'file://' + os.path.abspath(v))
    pages.append(s.replace('display:flex;flex-direction:column', 'display:flex;flex-direction:column', 1))
doc = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Amiri;src:url(file://{font}/Amiri-Regular.ttf);font-weight:400}}
@font-face{{font-family:Amiri;src:url(file://{font}/Amiri-Bold.ttf);font-weight:700}}
@page{{size:1920px 1080px;margin:0}}*{{box-sizing:border-box;margin:0}}
section p,section h1,section h2,section h3{{direction:rtl;unicode-bidi:plaintext}}
section{{width:1920px;height:1080px;position:relative;overflow:hidden;page-break-after:always}}
</style></head><body>{''.join(pages)}</body></html>'''
tmp = '/tmp/deck_render.html'; open(tmp, 'w', encoding='utf-8').write(doc)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto('file://' + tmp); pg.wait_for_timeout(1500)
    pg.pdf(path=out_pdf, width='1920px', height='1080px', print_background=True); b.close()
open(out_notes, 'w', encoding='utf-8').write(f'# ملاحظات المتحدث: {deck["title"]}\n\n' + '\n'.join(notes))
print(out_pdf, len(pages))
