#!/usr/bin/env python3
"""يبني ملف الوحدة 5 (PDF) بنفس تصميم بطاقات المصنع. التشغيل: python packages/video/unit-5/build_pdf.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'studio'))
import make_video as M
from playwright.sync_api import sync_playwright
import pymupdf

T = M.THEMES['video']; LABEL = 'مسار الفيديو · الوحدة 5: المونتاج والإضافات'
OUT = os.path.join(ROOT, 'resources/video/video-unit-5.pdf')
E = lambda s: M.em(s, T)
H1 = lambda t: f'<h1 style="position:absolute;top:150px;right:110px">{E(t)}</h1>'
BOX = f'background:{T["PAPER"]};border:3px solid {T["LINE"]};border-radius:24px'

def table(head, rows, widths, fs=38):
    th = ''.join(f'<th style="width:{w};background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:32px;padding:14px 18px;text-align:right">{h}</th>' for h, w in zip(head, widths))
    tr = ''.join('<tr>' + ''.join(f'<td style="border:2px solid {T["LINE"]};padding:12px 18px;font-size:{fs}px;line-height:1.4;vertical-align:top">{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table style="width:100%;border-collapse:collapse;background:#fff"><tr>{th}</tr>{tr}</table>'



import json
def cover():
    goals = ''.join(f'<li style="margin-bottom:10px">{g}</li>' for g in [
        'تجمع مشاهدك على صوتك بخمس خطوات.', 'تختار من الإضافات ما في بطاقتك فقط.',
        'تستخدم الموسيقى والخطوط بترخيص محفوظ.', 'تصدّر النسخة v1 وتحفظ مجلد المشروع.'])
    return f"""<div style="position:absolute;top:190px;right:110px;left:110px">
<div style="display:inline-block;background:{T['ACC']};color:#fff;font-family:Tajawal;font-size:44px;border-radius:16px;padding:8px 30px">الوحدة 5 · المونتاج والإضافات</div>
<div style="font-size:130px;font-weight:700;line-height:1.1;margin-top:20px">{E('المونتاج [[والإضافات]]')}</div>
<div style="display:flex;gap:40px;margin-top:40px">
<div style="flex:1.2;{BOX};padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">ستكون قادرًا على</div><ol style="font-size:42px;line-height:1.45;margin:14px 0 0;padding-right:50px">{goals}</ol></div>
<div style="flex:1;border:4px solid {T['GRN']};border-radius:24px;padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">تخرج من الوحدة بـ</div>
<div style="font-size:46px;line-height:1.6;margin-top:14px;font-weight:700;color:{T['GRN']}">الفيديو كاملًا<br>نسخة v1 مصدّرة<br>ومجلد مشروع محفوظ</div></div></div></div>"""

SPEC = json.load(open(os.path.join(ROOT, 'productions/video-unit-5/spec.json'), encoding='utf-8'))
CARDS = []
for s in SPEC['segments']:
    if s['type'] == 'card':
        c = dict(s['card']); c.pop('reveal_at', None); CARDS.append(c)

def addons_table():
    rows = [['1','ترجمة نصية','دائمًا تقريبًا: كثيرون يشاهدون بلا صوت','مجاني'],['2','موسيقى','الإعلان، والتهنئة، وملخص الفعالية · نادرًا في الدرس','مجاني إلى اشتراك'],
            ['3','مؤثرات صوتية','لحظة تريد لفت الانتباه إليها','مجاني'],['4','شعار وهوية','فيديو لجهة، أو سلسلة','مجاني'],
            ['5','مقدمة وخاتمة','كل فيديو منشور، وخطوة واحدة في الختام','مجاني'],['6','نسخة عمودية أو مربعة','تيك توك، وإنستغرام، وShorts','مجاني'],
            ['7–8','الصورة المصغرة · العنوان والوصف','في الوحدة 6: التحقق والنشر','—']]
    return H1('الإضافات [[الثماني]] في لمحة') + f"""<div style="position:absolute;top:290px;right:110px;left:110px">{table(["#","الإضافة","متى تحتاجها","فئة التكلفة"], rows, ["7%","27%","44%","22%"], 32)}
<div style="margin-top:20px;{BOX};padding:16px 30px;font-size:36px"><b style="color:{T['ACC']}">القاعدة:</b> أضف ما كتبته في بطاقتك فقط. كل إضافة لا يحتاجها الغرض تشتّت المشاهد وتأخذ وقتك.</div></div>"""

A1 = [('1. ترجمة نصية','ولّدها تلقائيًا ثم صحّحها سطرًا سطرًا من نصك. سطران بحد أقصى وخط كبير. محروقة في الصورة، أو ملف SRT يُشغَّل ويُطفأ ويسمح بأكثر من لغة.'),
      ('2. موسيقى','مرخّصة فقط: مكتبة يوتيوب الصوتية، وPixabay Music، أو اشتراك مثل Epidemic Sound وArtlist. بلا كلمات تحت الكلام. مثال للمستوى: الكلام نحو −6 ديسيبل، والموسيقى نحو −20 إلى −25. احفظ الترخيص.'),
      ('3. مؤثرات صوتية','مؤثر قصير مع عنصر مهم. القليل يلفت الانتباه، والكثير يزعج. من مصدر مرخّص.')]
A2 = [('4. شعار وهوية','شعار صغير في زاوية ثابتة بشفافية خفيفة. ألوان وخط ثابتة في السلسلة، وتحقق من رخصة الخط. احفظ قالبًا تعيد استخدامه.'),
      ('5. مقدمة وخاتمة','المقدمة ثانيتان إلى خمس، أو ابدأ بالوعد مباشرة. الخاتمة خطوة واحدة. على يوتيوب اترك 5 إلى 20 ثانية لشاشة النهاية إن أردتها.'),
      ('6. نسخة عمودية','لا تقصّ الأفقي: افتح مشروعًا 1080×1920 وأعد الترتيب. أبعد النص عن الأسفل والجانب الأيمن. تحقق من حد المدة الحالي قبل التصدير، فهو يتغير.')]

def export_page():
    rows = [['الصيغة','MP4 (H.264)، والصوت AAC'],['الدقة','1920×1080 أو 1080×1920، كما صممت'],['معدل الإطارات','معدل المشروع نفسه (غالبًا 30)'],
            ['الجودة','«عالية» أو «موصى بها». مثال: دقيقة بدقة 1080 تقارب 50 إلى 100 ميغابايت'],['الاسم','اسم-الفيديو-v1.mp4، ولكل تعديل رقم جديد']]
    return H1('[[التصدير]] والحفظ') + f"""<div style="position:absolute;top:290px;right:110px;left:110px">{table(["الإعداد","المقترح"], rows, ["26%","74%"], 36)}
<div style="margin-top:20px;border:4px solid {T['RED'] if 'RED' in T else T['ACC']};border-radius:24px;padding:16px 30px;font-size:34px;line-height:1.55"><b>احفظ مجلد المشروع كاملًا:</b> ملف المحرر، والصوت، والمشاهد، والموسيقى وتراخيصها، وملف SRT، ونسخة احتياطية في سحابة أو قرص. دون الملفات الأصلية لا تعديل بعد اليوم.</div></div>"""

def draft_page():
    rows = [['1','المسودة الثابتة: صورة المقدّم مكان الأفاتار، بالصوت والبطاقات النهائية','نحو 147 ث','مجاني'],
            ['2','مراجعة المسودة: النص، والتزامن، والتشكيل، والبطاقات','دقائق','مجاني'],
            ['3','توليد الأفاتار المتحرك للافتتاح والختام فقط، بعد الاعتماد','نحو 27 ث','≈ 1.9 $']]
    return H1('راجع مسودة [[ثابتة]] قبل أن تدفع مقابل التحريك') + f"""<div style="position:absolute;top:300px;right:110px;left:110px">
<div style="font-size:34px;line-height:1.55;margin-bottom:16px">التحريك (الأفاتار، والمشاهد المولّدة) هو الجزء المدفوع. وأي خطأ يُكتشف بعده يعني أن تدفع مرة أخرى. هذا ما فعلناه في هذه الوحدة نفسها:</div>
{table(['#','الخطوة','المدة','التكلفة'], rows, ['6%','58%','16%','20%'], 33)}
<div style="margin-top:18px;{BOX};padding:16px 30px;font-size:33px;line-height:1.55"><b style="color:{T['ACC']}">القاعدة:</b> ركّب الفيديو كاملًا أولًا بصورة ثابتة مكان كل مقطع مدفوع، وشاهده بسماعة. صحّح كل شيء وهو مجاني، ثم ولّد التحريك مرة واحدة.</div></div>"""

PROMPT = """هذه بطاقة فيديو: [الصق البطاقة]. وهذا جدول المشاهد مع مدة كل مشهد: [الصق الجدول].
الإضافات المختارة: [الإضافات]. المحرر الذي أستخدمه: [المحرر]. المنصة: [المنصة].
1. اكتب خطوات التجميع بالترتيب في هذا المحرر.
2. اكتب خطوات كل إضافة مختارة، ولا تقترح إضافة ليست في البطاقة.
3. اقترح إعدادات التصدير المناسبة لمنصتي.
4. نبّهني إلى كل إضافة تحتاج ترخيصًا، وأين أحفظه."""

def prompt_page():
    lines = PROMPT.replace('\n', '<br>')
    return H1('برومبت [[جاهز]]') + f"""<div style="position:absolute;top:290px;right:110px;left:110px;border:4px dashed {T['SEC']};border-radius:26px;background:#fff;padding:26px 40px;font-size:38px;line-height:1.6">{lines}</div>
<div style="position:absolute;bottom:100px;left:110px;font-family:Tajawal;font-size:28px;color:{T['MUT']}">انسخه والصقه في Claude أو ChatGPT، ثم راجع الناتج بقائمة التحقق.</div>"""

def mistakes_page():
    items = [('قص الصوت ليناسب المشاهد','كلام مبتور وإيقاع غير طبيعي','الصوت أولًا، والمشاهد تُقص عليه'),('انتقال بين كل مشهدين','فيديو بطيء يبدو هاويًا','قطع مباشر، وانتقال بين الأقسام فقط'),
             ('ترجمة تلقائية بلا مراجعة','أخطاء في الأسماء يراها الجميع','صحّحها من نصك المكتوب'),('موسيقى من الإنترنت بلا ترخيص','مطالبة حقوق، أو كتم، أو حجب','مصدر مرخّص، واحفظ الترخيص'),
             ('موسيقى أعلى من الكلام','المشاهد لا يفهم فيغادر','اختبر بسماعة، وخفّضها'),('قص الأفقي إلى عمودي','نص ووجه خارج الإطار','مشروع عمودي بترتيب جديد'),
             ('حذف ملفات المشروع بعد التصدير','لا تعديل ممكن لاحقًا','مجلد كامل ونسخة احتياطية')]
    rows = [[f'<b>{a}</b>', b, f'<b style="color:{T["GRN"]}">{c}</b>'] for a, b, c in items]
    return H1('أخطاء [[شائعة]]… وكيف تتجنبها') + f'<div style="position:absolute;top:300px;right:110px;left:110px">{table(["الخطأ","ماذا يحدث","كيف تتجنبه"], rows, ["34%","30%","36%"], 31)}</div>'

def check_page():
    items = ['وضعت الصوت أولًا ورتبت المشاهد عليه','قطعت الصمت والتكرار','شاهدت الفيديو كاملًا قبل الإضافات','صحّحت الترجمة النصية',
             'الموسيقى مرخّصة وتحت الكلام','أضفت ما في بطاقتي فقط','صدّرت v1 بالإعدادات المقترحة','حفظت مجلد المشروع ونسخة احتياطية']
    li = ''.join(f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:10px;font-size:40px"><span id="ck{i}" style="width:46px;height:46px;border:4px solid {T["INK"]};border-radius:10px;flex:none"></span>{x}</div>' for i, x in enumerate(items))
    return H1('قبل أن تنتقل إلى [[الوحدة 6]]') + f'<div style="position:absolute;top:280px;right:130px">{li}</div>', [(f'ck{i}', 'check') for i in range(len(items))]

ADD = ['ترجمة نصية','موسيقى','مؤثرات صوتية','شعار وهوية','مقدمة وخاتمة','نسخة عمودية']
def worksheet():
    f = lambda i, w, h=54: f'<span id="{i}" style="display:inline-block;width:{w}px;height:{h}px;border-bottom:3px dotted {T["MUT"]};vertical-align:bottom"></span>'
    td = f'border:2px solid {T["LINE"]};padding:6px 12px'
    rows = ''.join(f'<tr><td style="{td};font-size:30px;width:24%">{a}</td><td style="{td};width:12%;text-align:center"><span id="in{k}" style="display:inline-block;width:40px;height:40px;border:3px solid {T["INK"]};border-radius:8px"></span></td><td style="{td};width:34%"><span id="src{k}" style="display:block;height:44px"></span></td><td style="{td};width:30%"><span id="lic{k}" style="display:block;height:44px"></span></td></tr>' for k, a in enumerate(ADD))
    th = ''.join(f'<th style="background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:28px;padding:10px 12px;text-align:right">{h}</th>' for h in ['الإضافة','في بطاقتي؟','المصدر أو الأداة','أين حفظت الترخيص'])
    html = H1('ورقة العمل: [[المونتاج]] الخاص بك') + f"""<div style="position:absolute;top:262px;right:110px;left:110px;font-size:31px;line-height:1.75">
الاسم: {f('name',380)} &nbsp; التاريخ: {f('date',220)} &nbsp; المحرر: {f('editor',360)}<br>
المنصة: {f('platform',300)} &nbsp; المقاس: {f('size',220)} &nbsp; مدة الفيديو: {f('dur',140)} ث &nbsp; اسم الملف: {f('fname',330)}<br>
<table style="width:100%;border-collapse:collapse;background:#fff;margin-top:8px"><tr>{th}</tr>{rows}</table>
<div style="margin-top:10px">مكان مجلد المشروع: {f('folder',560)} &nbsp; النسخة الاحتياطية: {f('backup',520)}</div></div>"""
    ids = [(x,'text') for x in ['name','date','editor','platform','size','dur','fname']] + [(f'in{k}','check') for k in range(6)] + [(f'{c}{k}','text') for k in range(6) for c in ('src','lic')] + [('folder','text'),('backup','text')]
    return html, ids

def pages():
    out = [(cover(), [])] + [(c, []) for c in CARDS]
    out += [(addons_table(), []), (forms_page('صفحة لكل [[إضافة]] (1)', A1), []), (forms_page('صفحة لكل [[إضافة]] (2)', A2), []),
            (export_page(), []), (draft_page(), []), (prompt_page(), []), (mistakes_page(), []), check_page(), worksheet()]
    return out

def forms_page(title, items):
    blocks = ''.join(f'<div style="{BOX};padding:16px 26px;margin-bottom:14px;break-inside:avoid;display:inline-block;width:100%;box-sizing:border-box"><div style="font-size:40px;font-weight:700;color:{T["ACC"]}">{h}</div><div style="font-size:31px;line-height:1.5">{b}</div></div>' for h, b in items)
    return H1(title) + f'<div style="position:absolute;top:290px;right:110px;left:110px;columns:2;column-gap:30px">{blocks}</div>'

def main():
    ps = pages(); n = len(ps); work = os.path.join(HERE, '_pdf'); os.makedirs(work, exist_ok=True); parts = []; boxes = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        for i, (body, ids) in enumerate(ps):
            scene = f'صفحة {i+1} من {n}'
            html = M.card_html(body, T, LABEL, scene) if isinstance(body, dict) else M.frame(T, LABEL, scene, body)
            fp = os.path.join(work, f'p{i}.html'); open(fp, 'w', encoding='utf-8').write(html)
            pg.goto('file://' + fp); pg.wait_for_timeout(300)
            bx = []
            for el, kind in ids:
                r = pg.locator('#' + el).bounding_box()
                if r: bx.append((el, kind, r))
            boxes.append(bx)
            pf = os.path.join(work, f'p{i}.pdf'); pg.pdf(path=pf, width='1920px', height='1080px', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
            parts.append(pf)
        b.close()
    doc = pymupdf.open()
    for pf in parts:
        d = pymupdf.open(pf); doc.insert_pdf(d, from_page=0, to_page=0)
    k = 0.75  # px → pt
    for i, bx in enumerate(boxes):
        page = doc[i]
        for el, kind, r in bx:
            w = pymupdf.Widget(); w.field_name = el
            w.rect = pymupdf.Rect(r['x']*k, r['y']*k, (r['x']+r['width'])*k, (r['y']+r['height'])*k)
            if kind == 'check':
                w.field_type = pymupdf.PDF_WIDGET_TYPE_CHECKBOX
            else:
                w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT; w.text_fontsize = 0; w.text_font = 'Helv'
            page.add_widget(w)
    doc.set_metadata({'title': 'مسار الفيديو · الوحدة 5: المونتاج والإضافات', 'author': 'منصة مسار'})
    doc.save(OUT, garbage=3, deflate=True); print('✓', OUT, doc.page_count, 'صفحات', sum(len(b) for b in boxes), 'حقلًا')

if __name__ == '__main__':
    main()
