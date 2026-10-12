#!/usr/bin/env python3
"""يبني ملف الوحدة 6 (PDF) بنفس تصميم بطاقات المصنع. التشغيل: python packages/video/unit-6/build_pdf.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'studio'))
import make_video as M
from playwright.sync_api import sync_playwright
import pymupdf

T = M.THEMES['video']; LABEL = 'مسار الفيديو · الوحدة 6: التحقق والنشر'
OUT = os.path.join(ROOT, 'resources/video/video-unit-6.pdf')
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
        'تفحص الفيديو الخاص بك على الهاتف بخمسة فحوص.', 'تجهّز الموافقات والإفصاح والتراخيص قبل النشر.',
        'تكتب عنوانًا ووصفًا وفصولًا وصورة مصغرة صحيحة.', 'تنشره غير مدرج ثم عامًا، وتكتب بطاقة القرار.'])
    return f"""<div style="position:absolute;top:190px;right:110px;left:110px">
<div style="display:inline-block;background:{T['ACC']};color:#fff;font-family:Tajawal;font-size:44px;border-radius:16px;padding:8px 30px">الوحدة 6 · التحقق والنشر</div>
<div style="font-size:130px;font-weight:700;line-height:1.1;margin-top:20px">{E('التحقق [[والنشر]]')}</div>
<div style="display:flex;gap:40px;margin-top:40px">
<div style="flex:1.2;{BOX};padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">ستكون قادرًا على</div><ol style="font-size:40px;line-height:1.45;margin:14px 0 0;padding-right:50px">{goals}</ol></div>
<div style="flex:1;border:4px solid {T['GRN']};border-radius:24px;padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">تخرج من الوحدة بـ</div>
<div style="font-size:46px;line-height:1.6;margin-top:14px;font-weight:700;color:{T['GRN']}">فيديو منشور<br>وبطاقة القرار<br>وحقيبة مكتملة</div></div></div></div>"""

SPEC = json.load(open(os.path.join(ROOT, 'productions/video-unit-6/spec.json'), encoding='utf-8'))
CARDS = []
for s in SPEC['segments']:
    if s['type'] == 'card':
        c = dict(s['card']); c.pop('reveal_at', None); CARDS.append(c)

def phone_page():
    rows = [['1','بسماعة','الكلام واضح؟ الموسيقى تحت الكلام؟ لا قطع ولا صمت طويل؟'],['2','بلا صوت','تُفهم الفكرة من الصورة والترجمة وحدهما؟ الترجمة تُقرأ على شاشة صغيرة؟'],
            ['3','الأطراف','النص المهم بعيد عن الحواف وعن أزرار المنصة؟'],['4','الأسماء والأرقام والروابط','راجعها واحدًا واحدًا مقابل نصك المكتوب'],
            ['5','مشاهد من جمهورك','يقول لك الرسالة الواحدة بكلماته بعد المشاهدة؟']]
    return H1('افحصه على [[الهاتف]]: خمسة فحوص') + f"""<div style="position:absolute;top:290px;right:110px;left:110px">
<div style="font-size:34px;margin-bottom:14px">أغلب المشاهدين على الهاتف، فالفحص على الحاسوب وحده لا يكفي.</div>
{table(["#","الفحص","ماذا تسأل"], rows, ["6%","26%","68%"], 33)}</div>"""

def rights_page():
    items = [('موافقة مكتوبة','من كل شخص يظهر أو يُسمع صوته، ومن ولي الأمر إن كان قاصرًا. رسالة واضحة تكفي (النموذج في الصفحة الأخيرة).'),
             ('الإفصاح عن المحتوى المولّد','يوتيوب يطلبه للمحتوى الواقعي الذي قد يظنه المشاهد حقيقيًا: شخص واقعي المظهر يقول أو يفعل ما لم يحدث، أو تعديل لقطات حقيقية، أو مشهد واقعي مولّد. الأفاتار الواقعي يحتاجه. لا يُطلب لكتابة النص أو الترجمة التلقائية بالذكاء الاصطناعي.'),
             ('التراخيص','الموسيقى والمؤثرات والخطوط والصور: الترخيص محفوظ في مجلد المشروع.'),
             ('«مخصص للأطفال؟»','سؤال إلزامي عند الرفع. أجب بحسب جمهورك الفعلي.')]
    return forms_page('قبل زر [[النشر]]', items)

def title_thumb_page():
    items = [('العنوان: لا تفعل','«فيديو جديد 2»، «الحلقة الثالثة»، أو عنوان طويل يُقص على الهاتف.'),
             ('العنوان: افعل','الوعد والكلمة التي يبحث عنها جمهورك أولًا، ثم اسم السلسلة. الحد الأقصى في يوتيوب 100 حرف، والظاهر على الهاتف أقصر بكثير.'),
             ('الصورة المصغرة: لا تفعل','لقطة عشوائية من منتصف الكلام، أو جملة طويلة بخط صغير، أو تكرار العنوان حرفيًا.'),
             ('الصورة المصغرة: افعل','وجه واضح، وكلمات قليلة بخط عريض، وتباين قوي. اختبرها بحجم إبهامك. لا تضع شيئًا مهمًا في الزاويتين السفليتين (مكان مدة الفيديو).'),
             ('المقاس','1280×720 بنسبة 16:9 (أقل عرض 640). حد حجم الملف يختلف ويتغير، فتحقق منه عند الرفع. تحتاج حسابًا موثقًا.')]
    return forms_page('العنوان والصورة [[المصغرة]]', items)

def desc_page():
    ex = '0:00 من المشاهد إلى الفيديو<br>0:10 التجميع في خمس خطوات<br>0:32 الإضافات<br>0:52 الترجمة النصية<br>1:10 الموسيقى'
    return H1('[[الوصف]] والفصول والوسوم') + f"""<div style="position:absolute;top:290px;right:110px;left:110px;display:flex;gap:36px">
<div style="flex:1.3;{BOX};padding:22px 34px;font-size:33px;line-height:1.6"><b style="color:{T['ACC']}">ترتيب الوصف:</b><br>① سطران: الوعد والفائدة (يظهران قبل «المزيد»)<br>② ما سيتعلمه المشاهد<br>③ المهمة أو الخطوة التالية<br>④ الفصول<br>⑤ الروابط: السابق والتالي<br>⑥ الإفصاح<br><b style="color:{T['ACC']}">الوسوم:</b> قليلة ودقيقة، وأثرها محدود.<br><b style="color:{T['ACC']}">الترجمة:</b> ارفع ملف SRT المصحّح.</div>
<div style="flex:1;border:4px solid {T['GRN']};border-radius:24px;padding:22px 34px;font-size:33px;line-height:1.6"><b style="color:{T['GRN']}">شروط الفصول في يوتيوب:</b><br>الأول 0:00 · ثلاثة على الأقل · 10 ثوانٍ أو أكثر لكل فصل. وإلا لا تظهر.<br><br><b>مثال من الوحدة 5 (مقاس من الفيديو النهائي):</b><div style="font-family:Tajawal;font-size:30px;margin-top:8px;direction:rtl">{ex}</div></div></div>"""

def publish_page():
    rows = [['1','ارفعه «غير مدرج»','لا يظهر في البحث، ويراه من معه الرابط فقط'],['2','أكمل التفاصيل','العنوان، والوصف والفصول، والصورة المصغرة، والترجمة، وسؤال الأطفال، والإفصاح'],
            ['3','شاهده من الرابط على هاتفك','ترى ما سيراه المشاهد بالضبط'],['4','اجعله «عامًا»','بعد أن يمر الفحص'],['5','قائمة التشغيل وشاشة النهاية','السلسلة بالترتيب، والفيديو التالي'],
            ['6','المنصات الأخرى','النسخة العمودية بعنوان ووصف أقصر']]
    return H1('النشر: [[غير مدرج]] أولًا') + f'<div style="position:absolute;top:290px;right:110px;left:110px">{table(["#","الخطوة","لماذا"], rows, ["6%","34%","60%"], 33)}</div>'

PROMPT = """هذه بطاقة فيديو: [الصق البطاقة]. وهذا نص الفيديو مع التوقيتات النهائية: [الصق]. والمنصة: [المنصة].
1. اقترح ثلاثة عناوين، الوعد والكلمة المهمة في أولها.
2. اقترح نصًا للصورة المصغرة من كلمتين إلى أربع، لا يكرر العنوان.
3. اكتب وصفًا يبدأ بسطرين يحملان الفائدة.
4. اكتب الفصول من توقيتاتي بشروط يوتيوب.
5. اذكر ما يحتاج موافقة أو إفصاحًا أو ترخيصًا في هذا الفيديو."""

def prompt_page():
    lines = PROMPT.replace('\n', '<br>')
    return H1('برومبت [[جاهز]]') + f"""<div style="position:absolute;top:290px;right:110px;left:110px;border:4px dashed {T['SEC']};border-radius:26px;background:#fff;padding:26px 40px;font-size:37px;line-height:1.6">{lines}</div>
<div style="position:absolute;bottom:100px;left:110px;font-family:Tajawal;font-size:28px;color:{T['MUT']}">انسخه والصقه في Claude أو ChatGPT، ثم راجع الناتج بقائمة التحقق.</div>"""

def mistakes_page():
    items = [('الفحص على الحاسوب فقط','نص لا يُقرأ وأطراف مقصوصة','افحص على الهاتف، بسماعة وبلا صوت'),('عنوان لا يعد بشيء','لا أحد ينقر','الوعد والكلمة المهمة أولًا'),
             ('صورة مصغرة مزدحمة','لا تُقرأ في البحث','وجه واحد وكلمات قليلة'),('فصول لا تبدأ من 0:00','لا تظهر الفصول','0:00، وثلاثة، و10 ثوانٍ لكل فصل'),
             ('نشر شخص بلا موافقة','طلب حذف أو مشكلة قانونية','موافقة مكتوبة قبل النشر'),('أفاتار واقعي بلا إفصاح','مخالفة لسياسة المنصة','فعّل الإفصاح واذكره في الوصف'),
             ('النشر «عامًا» مباشرة','يرى الجميع الخطأ قبلك','غير مدرج أولًا، ثم عام'),('نسيان المشروع بعد النشر','تكرار الأخطاء نفسها','بطاقة القرار')]
    rows = [[f'<b>{a}</b>', b, f'<b style="color:{T["GRN"]}">{c}</b>'] for a, b, c in items]
    return H1('أخطاء [[شائعة]]… وكيف تتجنبها') + f'<div style="position:absolute;top:290px;right:110px;left:110px">{table(["الخطأ","ماذا يحدث","كيف تتجنبه"], rows, ["34%","30%","36%"], 30)}</div>'

def check_page():
    items = ['فحصت على الهاتف بسماعة وبلا صوت','راجعت الأسماء والأرقام والروابط','شاهده شخص من جمهوري وقال الرسالة','الموافقات محفوظة، والإفصاح مفعّل إن لزم',
             'عنوان بوعد واضح، وصورة مصغرة تُقرأ صغيرة','وصف وفصول بشروط يوتيوب، وملف الترجمة','نشرته غير مدرج ثم عامًا','كتبت بطاقة القرار']
    li = ''.join(f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:10px;font-size:39px"><span id="ck{i}" style="width:46px;height:46px;border:4px solid {T["INK"]};border-radius:10px;flex:none"></span>{x}</div>' for i, x in enumerate(items))
    return H1('قبل أن تضغط «[[عام]]»') + f'<div style="position:absolute;top:280px;right:130px">{li}</div>', [(f'ck{i}', 'check') for i in range(len(items))]

def decision_card():
    td = f'border:2px solid {T["LINE"]};padding:6px 14px'
    rows = [('الرابط ومستوى العرض','link'),('الرسالة الواحدة: هل وصلت؟','msg'),('المدة: المخططة ← الفعلية','dur'),('التكلفة: المتوقعة ← الفعلية، وسبب الفرق','cost'),
            ('ما نجح (أكرره)','good'),('ما أودّ تغييره (خطوة واحدة)','change'),('بعد أسبوع: المشاهدات · متوسط المشاهدة · تعليق مفيد','week')]
    tr = ''.join(f'<tr><td style="{td};font-size:30px;width:36%;background:{T["PAPER"]}"><b>{a}</b></td><td style="{td};width:64%"><span id="{k}" style="display:block;height:50px"></span></td></tr>' for a, k in rows)
    opts = ['أكرر الطريقة نفسها','أغيّر الشكل','أغيّر الأداة','أغيّر الجمهور']
    ch = ''.join(f'<span style="display:inline-flex;align-items:center;gap:12px;margin-left:34px"><span id="dc{i}" style="width:40px;height:40px;border:3px solid {T["INK"]};border-radius:8px;display:inline-block"></span>{o}</span>' for i, o in enumerate(opts))
    html = H1('بطاقة [[القرار]]') + f"""<div style="position:absolute;top:262px;right:110px;left:110px;font-size:30px">
<div style="margin-bottom:8px;color:{T['MUT']}">تقارن بطاقة الفيديو (الوحدة 1) بما حدث فعلًا، وتغلق المشروع.</div>
<table style="width:100%;border-collapse:collapse;background:#fff">{tr}</table>
<div style="margin-top:14px;font-size:32px"><b>القرار للفيديو القادم:</b> {ch}</div></div>"""
    return html, [(k, 'text') for _, k in rows] + [(f'dc{i}', 'check') for i in range(4)]

def consent_page():
    f = lambda i, w: f'<span id="{i}" style="display:inline-block;width:{w}px;height:52px;border-bottom:3px dotted {T["MUT"]};vertical-align:bottom"></span>'
    html = H1('نموذج [[موافقة]] على الظهور') + f"""<div style="position:absolute;top:300px;right:130px;left:130px;{BOX};padding:34px 46px;font-size:36px;line-height:2.1">
أنا {f('cn_name',560)}، أوافق على ظهوري (صورةً أو صوتًا)<br>في الفيديو {f('cn_video',700)}<br>
الذي يُنشر على {f('cn_platform',380)} باسم {f('cn_owner',460)}.<br>
<span style="font-size:30px;color:{T['MUT']}">وإن كان المشارك قاصرًا، يوقّع ولي أمره.</span><br>
التوقيع: {f('cn_sign',420)} &nbsp; التاريخ: {f('cn_date',280)}<br>ولي الأمر (إن لزم): {f('cn_guard',520)}</div>"""
    return html, [(x, 'text') for x in ['cn_name','cn_video','cn_platform','cn_owner','cn_sign','cn_date','cn_guard']]

def pages():
    out = [(cover(), [])] + [(c, []) for c in CARDS]
    out += [(phone_page(), []), (rights_page(), []), (title_thumb_page(), []), (desc_page(), []), (publish_page(), []),
            (prompt_page(), []), (mistakes_page(), []), check_page(), decision_card(), consent_page()]
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
    doc.set_metadata({'title': 'مسار الفيديو · الوحدة 6: التحقق والنشر', 'author': 'منصة مسار'})
    doc.save(OUT, garbage=3, deflate=True); print('✓', OUT, doc.page_count, 'صفحات', sum(len(b) for b in boxes), 'حقلًا')

if __name__ == '__main__':
    main()
