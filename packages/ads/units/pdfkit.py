#!/usr/bin/env python3
"""أدوات مشتركة لملفات وحدات حقيبة الإعلانات (PDF) بقالب بطاقات المصنع، على نسق ملفات حقيبة الفيديو.
كل وحدة تستورد هذا الملف من build_pdf.py الخاص بها."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'studio'))
import make_video as M

T = M.THEMES['ads']
E = lambda s: M.em(s, T)
H1 = lambda t: f'<h1 style="position:absolute;top:150px;right:110px">{E(t)}</h1>'
BOX = f'background:{T["PAPER"]};border:3px solid {T["LINE"]};border-radius:24px'
LINE = f'border-bottom:3px dotted {T["MUT"]};display:inline-block'

# حقول قابلة للكتابة (قاعدة المصنع منذ الوحدة 3 من حقيبة الفيديو): كل عنصر فيه data-f يصير حقلًا حقيقيًا في PDF.
def fx(w, h=48):
    """سطر كتابة داخل النص."""
    return f'<span data-f="t" style="display:inline-block;width:{w}px;height:{h}px;border-bottom:3px dotted {T["MUT"]};vertical-align:bottom"></span>'

def cell(h=70):
    """خانة كتابة تملأ خلية الجدول."""
    return f'<span data-f="t" style="display:block;height:{h}px"></span>'

def fc(size=40):
    """مربع اختيار."""
    return f'<span data-f="c" style="display:inline-block;width:{size}px;height:{size}px;border:3px solid {T["INK"]};border-radius:8px;vertical-align:middle;margin-left:10px"></span>'


def cover(badge, title, goals, outs):
    li = ''.join(f'<li style="margin-bottom:10px">{g}</li>' for g in goals)
    return f'''<div style="position:absolute;top:190px;right:110px;left:110px">
<div style="display:inline-block;background:{T['ACC']};color:#fff;font-family:Tajawal;font-size:44px;border-radius:16px;padding:8px 30px">{badge}</div>
<div style="font-size:140px;font-weight:700;line-height:1.1;margin-top:20px">{E(title)}</div>
<div style="display:flex;gap:40px;margin-top:40px">
<div style="flex:1.3;{BOX};padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">ستكون قادرًا على</div><ol style="font-size:42px;line-height:1.45;margin:14px 0 0;padding-right:50px">{li}</ol></div>
<div style="flex:1;border:4px solid {T['GRN']};border-radius:24px;padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">تخرج من الوحدة بـ</div>
<div style="font-size:44px;line-height:1.6;margin-top:14px;font-weight:700;color:{T['GRN']}">{outs}</div></div></div></div>'''


def compare(c):
    def side(s, col):
        q = '«%s»' % s['text'] if c.get('quote', True) else s['text']
        return f'''<div style="flex:1;border:5px solid {col};border-radius:28px;background:#fff;padding:30px 40px">
<div style="display:inline-block;background:{col};color:#fff;font-family:Tajawal;font-size:38px;border-radius:14px;padding:6px 26px">{s['label']}</div>
<div style="font-size:48px;line-height:1.5;margin-top:22px;min-height:300px">{q}</div>
<div style="font-size:42px;font-weight:700;color:{col};border-top:3px solid {T['LINE']};padding-top:16px">{s['verdict']}</div></div>'''
    return H1(c['title']) + f'<div style="position:absolute;top:340px;right:110px;left:110px;display:flex;gap:40px">{side(c["before"],T["ACC"])}{side(c["after"],T["GRN"])}</div>'


def table(head, rows, widths, fs=36, hfs=32):
    th = ''.join(f'<th style="width:{w};background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:{hfs}px;padding:12px 16px;text-align:right">{h}</th>' for h, w in zip(head, widths))
    tr = ''.join('<tr>' + ''.join(f'<td style="border:2px solid {T["LINE"]};padding:10px 16px;font-size:{fs}px;line-height:1.35;vertical-align:top">{x}</td>' for x in r) + '</tr>' for r in rows)
    return f'<table style="width:100%;border-collapse:collapse;background:#fff"><tr>{th}</tr>{tr}</table>'


def table_page(title, head, rows, widths, fs=36, note='', top=300):
    n = f'<div style="margin-top:20px;{BOX};padding:16px 28px;font-size:32px;line-height:1.5">{E(note)}</div>' if note else ''
    return H1(title) + f'<div style="position:absolute;top:{top}px;right:110px;left:110px">{table(head, rows, widths, fs)}{n}</div>'


def blocks_page(title, items, cols=2, fs=32):
    b = ''.join(f'<div style="{BOX};padding:20px 28px"><div style="font-size:40px;font-weight:700;color:{T["ACC"]}">{h}</div><div style="font-size:{fs}px;line-height:1.5">{x}</div></div>' for h, x in items)
    return H1(title) + f'<div style="position:absolute;top:290px;right:110px;left:110px;display:grid;grid-template-columns:repeat({cols},1fr);gap:24px">{b}</div>'


def prompt_page(prompt, footer, fs=32):
    lines = prompt.replace('\n', '<br>')
    return H1('برومبت [[جاهز]]') + f'''<div style="position:absolute;top:290px;right:110px;left:110px;border:4px dashed {T['SEC']};border-radius:26px;background:#fff;padding:24px 40px;font-size:{fs}px;line-height:1.5">{lines}</div>
<div style="position:absolute;bottom:90px;right:110px;left:110px;font-family:Tajawal;font-size:28px;color:{T['MUT']}">{footer}</div>'''


def mistakes_page(items, title='أخطاء [[شائعة]]… وكيف تتجنبها', fs=34):
    rows = [[f'<b>{a}</b>', b, f'<b style="color:{T["GRN"]}">{c}</b>'] for a, b, c in items]
    return table_page(title, ['الخطأ', 'ماذا يحدث', 'كيف تتجنبه'], rows, ['28%', '40%', '32%'], fs, top=310)


def check_page(title, items, fs=46):
    li = ''.join(f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:22px;font-size:{fs}px"><span data-f="c" style="width:50px;height:50px;border:4px solid {T["INK"]};border-radius:10px;flex:none"></span>{x}</div>' for x in items)
    return H1(title) + f'<div style="position:absolute;top:320px;right:130px;left:130px">{li}</div>'


def name_line(top=290):
    return f'<div style="position:absolute;top:{top}px;right:110px;font-size:34px">الاسم: {fx(360, 44)}&nbsp;&nbsp; التاريخ: {fx(220, 44)}</div>'


def build(pages, label, out, title):
    from playwright.sync_api import sync_playwright
    import pymupdf
    n = len(pages); work = os.path.join(os.path.dirname(out), '_pdf_' + os.path.basename(out)[:-4]); os.makedirs(work, exist_ok=True); parts = []; boxes = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        for i, body in enumerate(pages):
            scene = f'صفحة {i+1} من {n}'
            html = M.card_html(body, T, label, scene) if isinstance(body, dict) else M.frame(T, label, scene, body)
            f = os.path.join(work, f'p{i}.html'); open(f, 'w', encoding='utf-8').write(html)
            pg.goto('file://' + f); pg.wait_for_timeout(300)
            # فحص الفيض: لا عنصر يتجاوز أسفل الصفحة
            over = pg.evaluate("Math.max(...[...document.querySelectorAll('body *')].map(e=>e.getBoundingClientRect().bottom))")
            if over > 1080: print(f'⚠ صفحة {i+1}: محتوى يتجاوز الأسفل ({int(over)}px)')
            boxes.append(pg.evaluate("[...document.querySelectorAll('[data-f]')].map(e=>{const r=e.getBoundingClientRect();return [e.dataset.f,r.x,r.y,r.width,r.height]})"))
            pf = os.path.join(work, f'p{i}.pdf'); pg.pdf(path=pf, width='1920px', height='1080px', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
            parts.append(pf)
        b.close()
    doc = pymupdf.open()
    for pf in parts:
        d = pymupdf.open(pf); doc.insert_pdf(d, from_page=0, to_page=0)
    k = 0.75; nf = 0  # px → pt
    for i, bx in enumerate(boxes):
        for j, (kind, x, y, w_, h_) in enumerate(bx):
            w = pymupdf.Widget(); w.field_name = f'p{i+1}_{kind}{j+1}'
            w.rect = pymupdf.Rect(x*k, y*k, (x+w_)*k, (y+h_)*k)
            if kind == 'c':
                w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
            else:
                w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT; w.text_fontsize = 0; w.text_font = 'Helv'
                if h_ > 60: w.field_flags = pymupdf.PDF_TX_FIELD_IS_MULTILINE; w.text_fontsize = 16
            doc[i].add_widget(w); nf += 1
            if kind != 'c': doc.xref_set_key(w.xref, 'Q', '2')  # محاذاة يمين للكتابة العربية
    doc.set_metadata({'title': title, 'author': 'منصة مسار'})
    os.makedirs(os.path.dirname(out), exist_ok=True)
    doc.save(out, garbage=3, deflate=True); print('✓', out, doc.page_count, 'صفحات', nf, 'حقلًا')
    import shutil; shutil.rmtree(work, ignore_errors=True)


def tangible_page(stage, make, test, carry, make_lines=2, title='[[طبّق]] الآن: من الفكرة إلى شيء يُرى'):
    """فقرة «الملموس» الثابتة في نهاية كل وحدة (سجل 263): أين وصل إعلان سَمَر · اصنع بيدك · اختبر بعين غيرك · احمله معك."""
    lines = '<br>'.join(fx(760, 44) for _ in range(make_lines))
    box = lambda h, x, extra='': f'<div style="{BOX};padding:20px 28px"><div style="font-size:38px;font-weight:700;color:{T["ACC"]}">{h}</div><div style="font-size:30px;line-height:1.5">{x}</div>{extra}</div>'
    return H1(title) + f'''<div style="position:absolute;top:280px;right:110px;left:110px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
{box('1. أين وصل إعلان «سَمَر»؟', stage)}
{box('2. اصنع بيدك <span style="font-size:26px;color:' + T['GRN'] + '">(مجانًا)</span>', make, f'<div style="font-size:28px;line-height:1.7;margin-top:6px">{lines}</div>')}
{box('3. جرّبه على شخص آخر', test, f'<div style="font-size:28px;line-height:1.7;margin-top:6px">قال: {fx(680, 44)}</div>')}
{box('4. خذه معك إلى الوحدة التالية', carry)}</div>'''
