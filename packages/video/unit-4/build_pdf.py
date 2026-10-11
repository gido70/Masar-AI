#!/usr/bin/env python3
"""يبني ملف الوحدة 4 (PDF) بنفس تصميم بطاقات المصنع. التشغيل: python packages/video/unit-4/build_pdf.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'studio'))
import make_video as M
from playwright.sync_api import sync_playwright
import pymupdf

T = M.THEMES['video']; LABEL = 'مسار الفيديو · الوحدة 4: الصورة'
OUT = os.path.join(ROOT, 'resources/video/video-unit-4.pdf')
E = lambda s: M.em(s, T)
H1 = lambda t: f'<h1 style="position:absolute;top:150px;right:110px">{E(t)}</h1>'
BOX = f'background:{T["PAPER"]};border:3px solid {T["LINE"]};border-radius:24px'

def table(head, rows, widths, fs=38):
    th = ''.join(f'<th style="width:{w};background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:32px;padding:14px 18px;text-align:right">{h}</th>' for h, w in zip(head, widths))
    tr = ''.join('<tr>' + ''.join(f'<td style="border:2px solid {T["LINE"]};padding:12px 18px;font-size:{fs}px;line-height:1.4;vertical-align:top">{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table style="width:100%;border-collapse:collapse;background:#fff"><tr>{th}</tr>{tr}</table>'



def cover():
    goals = ''.join(f'<li style="margin-bottom:10px">{g}</li>' for g in [
        'تعرف عشرة أشكال للصورة وما يناسب كلًا منها.', 'تحسب تكلفة الشكل قبل أي توليد.',
        'تختار شكلك حسب الغرض في بطاقتك.', 'تجهّز مشاهدك على مدة صوتك.'])
    return f'''<div style="position:absolute;top:190px;right:110px;left:110px">
<div style="display:inline-block;background:{T['ACC']};color:#fff;font-family:Tajawal;font-size:44px;border-radius:16px;padding:8px 30px">الوحدة 4 · الصورة</div>
<div style="font-size:140px;font-weight:700;line-height:1.1;margin-top:20px">{E('الصورة: [[عشرة]] أشكال')}</div>
<div style="display:flex;gap:40px;margin-top:40px">
<div style="flex:1.2;{BOX};padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">ستكون قادرًا على</div><ol style="font-size:42px;line-height:1.45;margin:14px 0 0;padding-right:50px">{goals}</ol></div>
<div style="flex:1;border:4px solid {T['GRN']};border-radius:24px;padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">تخرج من الوحدة بـ</div>
<div style="font-size:46px;line-height:1.6;margin-top:14px;font-weight:700;color:{T['GRN']}">مشاهد جاهزة<br>بمدة صوتك<br>جاهزة للمونتاج</div></div></div></div>'''

def forms_table():
    rows = [['1','شرائح مع صوت','الدرس، والشرح، والتقرير','مجاني'],['2','أفاتار','الدرس المتكرر، والإعلان القصير، والسلسلة','الأغلى'],
            ['3','أمام الكاميرا','المقابلة، والشهادة، والتعريف بنفسك','مجاني'],['4','تسجيل الشاشة','شرح برنامج أو موقع','مجاني'],
            ['5','رسم باليد','فكرة تتكوّن تدريجيًا','مجاني · الأدوات باشتراك'],['6','رسوم متحركة','الإعلان، والفكرة المجردة، والأطفال','مجاني للبسيط · الأغلى للاحترافي'],
            ['7','مشاهد مولّدة','الإعلان، والقصة، والمشهد الذي لا تستطيع تصويره','الأغلى'],['8','صور متحركة','القصة، والتاريخ، والتهنئة','مجاني بصورك · سنتات إن ولّدتها'],
            ['9','مونتاج لقطات','ملخص الفعالية، والتعريف بجهة','مجاني'],['10','ترجمة أو دبلجة','فيديو موجود بلغة أخرى','الترجمة مجانية غالبًا · الدبلجة الأغلى']]
    return H1('الأشكال [[العشرة]] في لمحة') + f'<div style="position:absolute;top:290px;right:110px;left:110px">{table(["#","الشكل","يناسب","فئة التكلفة"], rows, ["5%","22%","43%","30%"], 31)}</div>'

def forms_page(title, items):
    blocks = ''.join(f'<div style="{BOX};padding:16px 26px;margin-bottom:14px;break-inside:avoid;display:inline-block;width:100%;box-sizing:border-box"><div style="font-size:40px;font-weight:700;color:{T["ACC"]}">{h}</div><div style="font-size:31px;line-height:1.5">{b}</div></div>' for h, b in items)
    return H1(title) + f'<div style="position:absolute;top:290px;right:110px;left:110px;columns:2;column-gap:30px">{blocks}</div>'

F1 = [('1. شرائح مع صوت','شريحة لكل جملة أو جملتين، وفكرة واحدة بكلمات قليلة. اضبط مدة كل شريحة على جملتها. PowerPoint أو Canva أو Google Slides.'),
      ('2. أفاتار','صورة واضحة للوجه وصوتك الجاهز. جرّب 10 ثوانٍ قبل الكل. الأغلى ويزيد مع المدة. الحوار بشخصين: لقطة لكل متكلم.'),
      ('3. أمام الكاميرا','النافذة أمامك، والهاتف بمستوى عينيك، وانظر إلى العدسة. صوّر مشهدًا مشهدًا.'),
      ('4. تسجيل الشاشة','وضع عدم الإزعاج، وأغلق النوافذ، وكبّر الخط. خطوة لكل جملة. OBS أو أداة هاتفك.'),
      ('5. رسم باليد','ورقة بيضاء وقلم عريض، والهاتف من الأعلى. خطّط الرسم على مسودة أولًا.')]
F2 = [('6. رسوم متحركة','ابدأ من قالب جاهز، وشخصية واحدة وألوان قليلة ثابتة. Canva للبسيط.'),
      ('7. مشاهد مولّدة','سطر لكل مشهد: المكان، والشخص، والحركة، والإضاءة، والزاوية. لقطة تجريبية واحدة قبل الكل. Veo وKling وRunway.'),
      ('8. صور متحركة','صورة لكل جملة تقريبًا، مع تقريب أو تحريك أفقي بطيء. CapCut مجاني.'),
      ('9. مونتاج لقطات','لقطات قصيرة 5 إلى 10 ثوانٍ، أفقية وثابتة، بزوايا متنوعة. اطلب إذن الظاهرين.'),
      ('10. ترجمة أو دبلجة','ابدأ من النص المكتوب، وراجع الترجمة بمتقن للغة. انتبه لطول الدبلجة.')]

def avatar_page():
    rows = [['الافتتاح (المقدّم وحده)','9 ث','≈ 0.6 $'],['الختام (المقدّم وحده)','18 ث','≈ 1.3 $'],['الحوار: لقطة لكل متكلم','37 ث','≈ 2.5 $']]
    return H1('الأفاتار: [[مثال]] مقاس من إنتاج هذه الوحدة') + f'''<div style="position:absolute;top:300px;right:110px;left:110px">
<div style="font-size:34px;line-height:1.55;margin-bottom:16px">أداة تحريك بالصوت بنحو 0.06 دولار للثانية. السعر للثانية ثابت، والمدة هي التي تكبر الفاتورة.</div>
{table(['المقطع','المدة','التكلفة'], rows, ['56%','20%','24%'], 36)}
<div style="margin-top:18px;{BOX};padding:16px 30px;font-size:33px;line-height:1.55"><b style="color:{T['ACC']}">ما تعلمناه:</b> شخصان في إطار واحد يتكلمان بالتناوب فشل في الأدوات المتاحة: الشفاه تتحرك عند الاثنين. الحل الذي نجح: <b>لقطة كاملة لكل متكلم</b>، كما في المقابلات التلفزيونية. والانتظار نحو نصف دقيقة لكل ثانية فيديو، فلا تضغط «توليد» مرتين.</div></div>'''

def camera_page():
    items = [('الإضاءة','النافذة أمامك أو بجانبك، لا خلفك. لا تخلط ضوءًا أصفر بأبيض.'),('الهاتف','الكاميرا الخلفية، وامسح العدسة، وحامل بمستوى العينين، و1080p بـ 30 إطارًا.'),
             ('الإطار','من منتصف الصدر، والعينان في الثلث العلوي، وابتعد عن الجدار مترًا.'),('الإلقاء','انظر إلى العدسة، وأبطأ قليلًا، وابتسم أول ثانية وآخرها.'),
             ('قبل التصوير','عشر ثوانٍ تجريبية تشاهدها بسماعة: وجه مضيء؟ صوت واضح؟ خلفية مرتبة؟')]
    return forms_page('أنت أمام [[الكاميرا]]', items)

PROMPT = '''هذه بطاقة فيديو: [الصق البطاقة]. وهذا جدول المشاهد مع مدة كل مشهد: [الصق الجدول]. الشكل المختار: [الشكل].
1. اقترح لكل مشهد ما يظهر على الشاشة بالتفصيل.
2. اقترح الأداة المناسبة لكل مشهد بفئة تكلفتها (مجاني، سنتات، الأغلى).
3. احسب تكلفة أي توليد مدفوع: سعر الثانية × مدة المشهد، ثم المجموع.
4. حدّد المشهد الذي يحتاج تجربة قصيرة قبل التوليد الكامل.'''

def prompt_page():
    lines = PROMPT.replace('\n', '<br>')
    return H1('برومبت [[جاهز]]') + f'''<div style="position:absolute;top:290px;right:110px;left:110px;border:4px dashed {T['SEC']};border-radius:26px;background:#fff;padding:26px 40px;font-size:38px;line-height:1.6">{lines}</div>
<div style="position:absolute;bottom:100px;left:110px;font-family:Tajawal;font-size:28px;color:{T['MUT']}">انسخه والصقه في Claude أو ChatGPT، ثم راجع الناتج بقائمة التحقق.</div>'''

def mistakes_page():
    items = [('اختيار الأداة قبل الشكل','شكل لا يناسب الغرض','الشكل من بطاقتك أولًا، ثم الأداة'),('توليد الفيديو كله مرة واحدة','خطأ واحد يعيد التكلفة كلها','مقطع تجريبي، ثم مقطعًا مقطعًا'),
             ('شريحة مزدحمة بالنص','المشاهد يقرأ ولا يسمع','فكرة واحدة وكلمات قليلة'),('تسجيل الشاشة مع الإشعارات','تظهر بيانات شخصية','عدم الإزعاج، وأغلق النوافذ'),
             ('شخصية تتغير بين المشاهد المولّدة','تبدو لأشخاص مختلفين','صورة مرجعية واحدة'),('مشاهد أطول أو أقصر من الصوت','فراغ أو قطع في المونتاج','مدة كل مشهد من ملف الصوت')]
    rows = [[f'<b>{a}</b>', b, f'<b style="color:{T["GRN"]}">{c}</b>'] for a, b, c in items]
    return H1('أخطاء [[شائعة]]… وكيف تتجنبها') + f'<div style="position:absolute;top:310px;right:110px;left:110px">{table(["الخطأ","ماذا يحدث","كيف تتجنبه"], rows, ["32%","32%","36%"], 34)}</div>'

def check_page():
    items = ['اخترت الشكل من بطاقتي','حسبت التكلفة قبل أي توليد','جرّبت مقطعًا أو مشهدًا واحدًا أولًا','جهّزت المشاهد مشهدًا مشهدًا',
             'طابقت مدة كل مشهد مع الصوت','تحققت من الحقوق والأذونات','حفظت المشاهد بأسماء مرتبة']
    li = ''.join(f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:12px;font-size:42px"><span id="ck{i}" style="width:48px;height:48px;border:4px solid {T["INK"]};border-radius:10px;flex:none"></span>{x}</div>' for i, x in enumerate(items))
    return H1('قبل أن تنتقل إلى [[الوحدة 5]]') + f'<div style="position:absolute;top:290px;right:130px">{li}</div>', [(f'ck{i}', 'check') for i in range(len(items))]

def worksheet():
    f = lambda i, w, h=54: f'<span id="{i}" style="display:inline-block;width:{w}px;height:{h}px;border-bottom:3px dotted {T["MUT"]};vertical-align:bottom"></span>'
    rows = ''.join(f'<tr><td style="border:2px solid {T["LINE"]};padding:6px 12px;font-size:30px;width:6%">{k}</td><td style="border:2px solid {T["LINE"]};width:44%"><span id="s{k}" style="display:block;height:44px"></span></td><td style="border:2px solid {T["LINE"]};width:20%"><span id="t{k}" style="display:block;height:44px"></span></td><td style="border:2px solid {T["LINE"]};width:12%"><span id="d{k}" style="display:block;height:44px"></span></td><td style="border:2px solid {T["LINE"]};width:18%"><span id="f{k}" style="display:block;height:44px"></span></td></tr>' for k in range(1, 7))
    th = ''.join(f'<th style="background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:28px;padding:10px 12px;text-align:right">{h}</th>' for h in ['#','ما يظهر على الشاشة','الأداة','ث','الملف'])
    html = H1('ورقة العمل: [[مشاهدك]]') + f'''<div style="position:absolute;top:262px;right:110px;left:110px;font-size:31px;line-height:1.75">
الاسم: {f('name',380)} &nbsp; التاريخ: {f('date',220)} &nbsp; الغرض في بطاقتك: {f('goal',380)}<br>
الشكل المختار: {f('form',420)} &nbsp; لماذا يناسب الغرض: {f('why',520)}<br>
التكلفة التقديرية: {f('rate',120)} $/ث × {f('secs',100)} ث = {f('cost',120)} $ &nbsp; مشهد التجربة: {f('test',300)}
<table style="width:100%;border-collapse:collapse;background:#fff;margin-top:8px"><tr>{th}</tr>{rows}</table></div>'''
    ids = [(x,'text') for x in ['name','date','goal','form','why','rate','secs','cost','test']] + [(f'{c}{k}','text') for k in range(1,7) for c in 'stdf']
    return html, ids

CARDS = [
 {"kind":"grid","title":"معرض [[الأشكال]]","cols":5,"items":[["شرائح","مع صوت"],["أفاتار","يتكلم بصوتك"],["أمام الكاميرا","أنت بنفسك"],["تسجيل الشاشة","خطوة خطوة"],["رسم باليد","يظهر أمامك"]]},
 {"kind":"grid","title":"معرض [[الأشكال]]","cols":5,"start":6,"items":[["رسوم متحركة","شخصيات وأشكال"],["مشاهد مولّدة","من وصف مكتوب"],["صور متحركة","حركة بطيئة"],["مونتاج لقطات","صوّرتها أنت"],["ترجمة أو دبلجة","لفيديو موجود"]]},
 {"kind":"cards","title":"[[تكلفة]] كل شكل","items":[["مجاني","الشرائح · الكاميرا · الشاشة · الرسم · لقطاتك","green"],["سنتات","الصور المتحركة","amber"],["الأغلى","الأفاتار · الرسوم · المشاهد المولّدة · الدبلجة","red"]],"warning":"<b style=\"color:#D62828\">قبل أي توليد:</b> سعر الثانية × عدد الثواني"},
 {"kind":"tree","title":"[[اختر]] شكلك","rows":[["درس","شرائح أو شاشة"],["شرح برنامج","تسجيل الشاشة"],["إعلان","مولّد أو أفاتار"],["مقابلة أو شهادة","أمام الكاميرا"]],"note":"شكلك مكتوب<br>في بطاقتك<br><b style=\"color:#D62828\">السؤال الرابع</b>"}]

def pages():
    out = [(cover(), [])] + [(c, []) for c in CARDS]
    out += [(forms_table(), []), (forms_page('صفحة لكل [[شكل]] (1)', F1), []), (forms_page('صفحة لكل [[شكل]] (2)', F2), []),
            (camera_page(), []), (avatar_page(), []), (prompt_page(), []), (mistakes_page(), []), check_page(), worksheet()]
    return out

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
    doc.set_metadata({'title': 'مسار الفيديو · الوحدة 4: الصورة', 'author': 'منصة مسار'})
    doc.save(OUT, garbage=3, deflate=True); print('✓', OUT, doc.page_count, 'صفحات', sum(len(b) for b in boxes), 'حقلًا')

if __name__ == '__main__':
    main()
