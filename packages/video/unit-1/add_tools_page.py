#!/usr/bin/env python3
"""يضيف صفحة «أدواتك في الحقيبة» إلى ملف الوحدة 1 قبل ورقة العمل (مرة واحدة فقط). التشغيل: python packages/video/unit-1/add_tools_page.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'studio')); import make_video as M
from playwright.sync_api import sync_playwright
import pymupdf
T = M.THEMES['video']; LABEL = 'مسار الفيديو · الوحدة 1: بطاقة الفيديو'
PDF = os.path.join(ROOT, 'resources/video/video-unit-1.pdf'); MARK = 'أدواتك في'
def table(head, rows, widths, fs):
    th = ''.join(f'<th style="width:{w};background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:30px;padding:12px 16px;text-align:right">{h}</th>' for h, w in zip(head, widths))
    tr = ''.join('<tr>' + ''.join(f'<td style="border:2px solid {T["LINE"]};padding:10px 16px;font-size:{fs}px;line-height:1.35;vertical-align:top">{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table style="width:100%;border-collapse:collapse;background:#fff"><tr>{th}</tr>{tr}</table>'
rows = [['1. البطاقة','ورقة العمل في هذا الملف، ثم Claude أو ChatGPT لمراجعتها','الورقة وحدها','مجاني'],
        ['2. النص','Google Docs أو Word، والتشكيل بـ Claude أو ChatGPT ثم مراجعتك','Google Docs','مجاني'],
        ['3. الصوت','صوت مولّد: ElevenLabs','صوتك بالهاتف، والتنظيف بـ Audacity','مجاني · سنتات للمولّد'],
        ['4. الصورة','حسب شكلك (صفحة لكل شكل في الوحدة 4)','الشرائح أو تسجيل الشاشة','مجاني إلى الأغلى'],
        ['5. المونتاج','CapCut للحاسوب والهاتف','DaVinci Resolve · Clipchamp · Canva','مجاني، وبعض الميزات باشتراك'],
        ['6. النشر','YouTube Studio','—','مجاني']]
body = f'''<h1 style="position:absolute;top:150px;right:110px">{M.em("أدواتك في [[الحقيبة]]: أداة وبديل مجاني", T)}</h1>
<div style="position:absolute;top:300px;right:110px;left:110px">{table(["المرحلة","الأداة الأساسية","البديل المجاني","فئة التكلفة"], rows, ["14%","42%","26%","18%"], 31)}
<div style="margin-top:16px;font-size:30px;color:{T['MUT']}">لكل مرحلة شرح مفصّل وخطوات في ملف وحدتها. الأسعار والميزات تتغير، فتحقق منها قبل الاشتراك.</div></div>'''
def main():
    doc = pymupdf.open(PDF)
    if any(MARK in p.get_text() for p in doc): print('• الصفحة موجودة، لا تغيير'); return
    n = doc.page_count + 1; work = os.path.join(HERE, '_pdf'); os.makedirs(work, exist_ok=True)
    html = M.frame(T, LABEL, f'صفحة {n - 1} من {n}', body); f = os.path.join(work, 'tools.html'); open(f, 'w', encoding='utf-8').write(html)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080}); pg.goto('file://' + f); pg.wait_for_timeout(400)
        pf = os.path.join(work, 'tools.pdf'); pg.pdf(path=pf, width='1920px', height='1080px', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'}); b.close()
    new = pymupdf.open(); new.insert_pdf(doc, from_page=0, to_page=doc.page_count - 2); new.insert_pdf(pymupdf.open(pf)); new.insert_pdf(doc, from_page=doc.page_count - 1, to_page=doc.page_count - 1)
    new.set_metadata(doc.metadata); doc.close(); new.save(PDF + '.tmp', garbage=3, deflate=True); os.replace(PDF + '.tmp', PDF); print('✓', PDF, new.page_count, 'صفحات')
if __name__ == '__main__': main()
