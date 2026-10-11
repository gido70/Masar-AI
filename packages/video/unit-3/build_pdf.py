#!/usr/bin/env python3
"""يبني ملف الوحدة 3 (PDF) بنفس تصميم بطاقات المصنع. التشغيل: python packages/video/unit-2/build_pdf.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'studio'))
import make_video as M
from playwright.sync_api import sync_playwright
import pymupdf

T = M.THEMES['video']; LABEL = 'مسار الفيديو · الوحدة 3: الصوت'
OUT = os.path.join(ROOT, 'resources/video/video-unit-3.pdf')
E = lambda s: M.em(s, T)
H1 = lambda t: f'<h1 style="position:absolute;top:150px;right:110px">{E(t)}</h1>'
BOX = f'background:{T["PAPER"]};border:3px solid {T["LINE"]};border-radius:24px'

def table(head, rows, widths, fs=38):
    th = ''.join(f'<th style="width:{w};background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:32px;padding:14px 18px;text-align:right">{h}</th>' for h, w in zip(head, widths))
    tr = ''.join('<tr>' + ''.join(f'<td style="border:2px solid {T["LINE"]};padding:12px 18px;font-size:{fs}px;line-height:1.4;vertical-align:top">{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table style="width:100%;border-collapse:collapse;background:#fff"><tr>{th}</tr>{tr}</table>'


FIELDS = []  # (page_index, element_id, kind)

def cover():
    goals = ''.join(f'<li style="margin-bottom:10px">{g}</li>' for g in [
        'تختار نوع الصوت المناسب لفيديوك.', 'تسجّل بصوتك في مكان مناسب، أو تولّد صوتًا بلا أخطاء نطق.',
        'تنظّف الصوت دون إفراط.', 'تقيس المدة وتقارنها ببطاقتك.'])
    return f'''<div style="position:absolute;top:190px;right:110px;left:110px">
<div style="display:inline-block;background:{T['ACC']};color:#fff;font-family:Tajawal;font-size:44px;border-radius:16px;padding:8px 30px">الوحدة 3 · الصوت</div>
<div style="font-size:140px;font-weight:700;line-height:1.1;margin-top:20px">{E('الصوت [[نصف]] الفيديو')}</div>
<div style="display:flex;gap:40px;margin-top:40px">
<div style="flex:1.2;{BOX};padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">ستكون قادرًا على</div><ol style="font-size:42px;line-height:1.45;margin:14px 0 0;padding-right:50px">{goals}</ol></div>
<div style="flex:1;border:4px solid {T['GRN']};border-radius:24px;padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">تخرج من الوحدة بـ</div>
<div style="font-size:46px;line-height:1.6;margin-top:14px;font-weight:700;color:{T['GRN']}">ملف صوت نهائي<br>مقاسة مدته<br>جاهز للمونتاج</div></div></div></div>'''

PROMPT = '''هذه بطاقة فيديو: [الصق بطاقتك]. وهذا النص: [الصق نصك من الوحدة 2].
1. ساعدني أختار بين: صوتي، أو صوت مولّد، أو دبلجة، أو بلا تعليق. اذكر السبب في سطرين.
2. استخرج أصعب جملتين في النطق، لأجربهما أولًا، واقترح بديلًا لكل منهما.
3. قسّم النص إلى مقاطع أسجّلها أو أولّدها مقطعًا مقطعًا، مع المدة المتوقعة لكل مقطع (الكلمات ÷ 1.8).
4. إن اخترت صوتي: أعطني قائمة تحقق قصيرة للمكان والهاتف قبل التسجيل.
5. إن اخترت صوتًا مولّدًا: ذكّرني بما أتحقق منه في شروط الاستخدام التجاري.'''

def prompt_page():
    lines = PROMPT.replace('\n', '<br>')
    return H1('برومبت [[جاهز]]') + f'''<div style="position:absolute;top:290px;right:110px;left:110px;border:4px dashed {T['SEC']};border-radius:26px;background:#fff;padding:26px 40px;font-size:36px;line-height:1.55">{lines}</div>
<div style="position:absolute;bottom:100px;left:110px;font-family:Tajawal;font-size:28px;color:{T['MUT']}">انسخه والصقه في Claude أو ChatGPT، ثم راجع الناتج بقائمة التحقق.</div>'''

def gear_page():
    rows = [['ميكروفون مشبك يوصَل بالهاتف', 'أكبر تحسين بأقل تكلفة: يقترب من فمك فيقلّ صدى الغرفة', 'منخفضة'],
            ['ميكروفون مشبك لاسلكي', 'الفائدة نفسها مع حرية الحركة أمام الكاميرا', 'متوسطة'],
            ['ميكروفون USB «ديناميكي»', 'يلتقط صوتك ويتجاهل الغرفة أكثر من «المكثّف»', 'متوسطة'],
            ['إسفنجة أو حاجز أمام الميكروفون', 'يمنع انفجار حرفَي الباء والفاء', 'منخفضة'],
            ['سماعة أذن سلكية', 'تسمع بها التسجيل وتكتشف الضوضاء', 'منخفضة']]
    return H1('معدات ترفع [[الجودة]] (اختيارية)') + f'''<div style="position:absolute;top:320px;right:110px;left:110px">{table(['المعدة','لماذا','فئة التكلفة'], rows, ['32%','52%','16%'], 36)}
<div style="margin-top:22px;{BOX};padding:18px 30px;font-size:38px"><b style="color:{T['ACC']}">القاعدة:</b> الغرفة الهادئة والميكروفون القريب أهم من الميكروفون الغالي.</div></div>'''

def tools_page():
    rows = [['ElevenLabs', 'صوت مولّد ودبلجة، ويدعم العربية', 'المجانية للتجربة وغير تجارية · الاستخدام التجاري من أرخص خطة مدفوعة · الدبلجة الأغلى'],
            ['Audacity', 'تسجيل وتنظيف وقياس المدة', 'مجاني'],
            ['مسجّل الصوت في هاتفك', 'البديل المجاني للتسجيل', 'مجاني']]
    return H1('الأدوات و[[التكلفة]]') + f'''<div style="position:absolute;top:320px;right:110px;left:110px">{table(['الأداة','لماذا','فئة التكلفة'], rows, ['22%','36%','42%'], 38)}
<div style="margin-top:22px;{BOX};padding:18px 30px;font-size:36px;line-height:1.5">الأسعار تتغير وتختلف بين الأدوات. احسب تكلفتك بنفسك: عدد أحرف نصك × سعر الحرف في الأداة، قبل أن تولّد.</div></div>'''

def example_page():
    rows = [['1', 'تريدُ فيديو لمشروعِك، لكنْ لا تعرفُ من أين تبدأْ؟', 'توليد', '3.6'],
            ['2', 'في ستِّ خطواتٍ تصنعُه بنفسِك: البطاقة، والنصّ، والصوت، والصورة، والمونتاج، والنشرْ.', 'توليد', '9.4'],
            ['3', 'بالذكاء الاصطناعي، وبتكلفةٍ تعرفُها قبلَ أن تضغطَ أيَّ زرّْ.', 'توليد', '5.1'],
            ['4', 'مسارُ الفيديو: أوّلُ فيديو لك جاهزٌ في نهايةِ الحقيبة. سجِّلِ الآنْ.', 'توليد', '6.2']]
    return H1('مثال [[مكتمل]]: صوت إعلان 30 ثانية') + f'''<div style="position:absolute;top:310px;right:110px;left:110px">
<div style="font-size:36px;margin-bottom:16px"><b>النوع:</b> صوت مولّد، لأن الإعلان سيُعدَّل لكل منصة. <b>جملتا الاختبار:</b> المقطعان 2 و4.</div>
{table(['#','المقطع (نسخة الصوت)','الطريقة','ث (مقاسة)'], rows, ['5%','63%','14%','18%'], 34)}
<div style="margin-top:18px;{BOX};padding:16px 30px;font-size:34px;line-height:1.5">المجموع 24.3 ث + فواصل قصيرة ≈ 27 ث، والبطاقة 30 ث: الفرق صغير، فلا حاجة لتعديل. الملف: voice-final.mp3</div></div>'''

def mistakes_page():
    items = [('تسجّل في غرفة فارغة', 'صدى لا تزيله أي أداة.', 'سجّل في غرفة فيها أثاث، أو أمام خزانة ملابس.'),
             ('تولّد النص كله مرة واحدة', 'خطأ في جملة يعيد الملف كله، وتضيع توقيتات الجمل.', 'ولّد جملة جملة أو مشهدًا مشهدًا.'),
             ('تغيّر الصوت بين فيديوهات السلسلة', 'تفقد السلسلة هويتها.', 'صوت واحد لكل السلسلة.'),
             ('تسرّع الصوت ليناسب المدة', 'يصير الصوت غير طبيعي.', 'اختصر النص.'),
             ('تنشر بخطة مجانية غير تجارية', 'تخالف شروط الأداة.', 'اقرأ شروط الاستخدام التجاري قبل النشر.')]
    rows = [[f'<b>{a}</b>', b, f'<b style="color:{T["GRN"]}">{c}</b>'] for a, b, c in items]
    return H1('أخطاء [[شائعة]]… وكيف تتجنبها') + f'<div style="position:absolute;top:320px;right:110px;left:110px">{table(["الخطأ","ماذا يحدث","كيف تتجنبه"], rows, ["28%","38%","34%"], 36)}</div>'

def check_page():
    items = ['اخترت نوع الصوت من بطاقتي', 'جرّبت جملتين أولًا', 'سجّلت أو ولّدت مقطعًا مقطعًا', 'نظّفت الصوت دون إفراط',
             'سمعته كاملًا بسماعة', 'قست المدة وقارنتها ببطاقتي', 'تحققت من حق الاستخدام', 'حفظت الملف باسم واضح']
    li = ''.join(f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:10px;font-size:40px"><span id="ck{i}" style="width:48px;height:48px;border:4px solid {T["INK"]};border-radius:10px;flex:none"></span>{x}</div>' for i, x in enumerate(items))
    return H1('قبل أن تنتقل إلى [[الوحدة 4]]') + f'<div style="position:absolute;top:290px;right:130px">{li}</div>', [(f'ck{i}', 'check') for i in range(len(items))]

def worksheet():
    f = lambda i, w, h=54: f'<span id="{i}" style="display:inline-block;width:{w}px;height:{h}px;border-bottom:3px dotted {T["MUT"]};vertical-align:bottom"></span>'
    box = lambda i: f'<span id="{i}" style="display:inline-block;width:40px;height:40px;border:3px solid {T["INK"]};border-radius:8px;vertical-align:middle;margin-left:10px"></span>'
    rows = ''.join(f'<tr><td style="border:2px solid {T["LINE"]};padding:6px 12px;font-size:30px;width:5%">{k}</td><td style="border:2px solid {T["LINE"]};width:62%"><span id="s{k}" style="display:block;height:44px"></span></td><td style="border:2px solid {T["LINE"]};width:18%"><span id="m{k}" style="display:block;height:44px"></span></td><td style="border:2px solid {T["LINE"]};width:15%"><span id="d{k}" style="display:block;height:44px"></span></td></tr>' for k in range(1, 6))
    th = ''.join(f'<th style="background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:28px;padding:10px 12px;text-align:right">{h}</th>' for h in ['#', 'المقطع', 'الطريقة', 'ث (مقاسة)'])
    html = H1('ورقة العمل: [[صوتك]]') + f'''<div style="position:absolute;top:262px;right:110px;left:110px;font-size:31px;line-height:1.75">
الاسم: {f('name',380)} &nbsp; التاريخ: {f('date',220)} &nbsp; مدة الفيديو في بطاقتك: {f('card',120)} ث<br>
نوع الصوت: {box('t1')}صوتي &nbsp; {box('t2')}مولّد &nbsp; {box('t3')}دبلجة &nbsp; {box('t4')}بلا تعليق &nbsp;&nbsp; السبب: {f('why',400)}<br>
جملتا الاختبار: ① {f('test1',560)} ② {f('test2',560)}
<table style="width:100%;border-collapse:collapse;background:#fff;margin-top:8px"><tr>{th}</tr>{rows}</table>
المدة الفعلية للملف: {f('total',140)} ث &nbsp; الفرق عن البطاقة: {f('diff',140)} ث &nbsp; اسم الملف: {f('file',330)}<br>{box('rights')}تحققت من حق الاستخدام قبل النشر</div>'''
    ids = [('name','text'),('date','text'),('card','text'),('why','text'),('test1','text'),('test2','text'),('total','text'),('diff','text'),('file','text'),('rights','check')]
    ids += [(f't{i}','check') for i in range(1,5)] + [(f'{c}{k}','text') for k in range(1,6) for c in 'smd']
    return html, ids

CARDS = [
 {"kind":"grid","title":"أربعة [[خيارات]] للصوت","cols":4,"items":[["صوتك","مجاني"],["صوت مولّد","سنتات"],["دبلجة","الأغلى"],["بلا تعليق","النص على الشاشة"]]},
 {"kind":"tree","title":"[[اختر]] صوتك","rows":[["وجهك في الفيديو","صوتك"],["سلسلة أو تعديلات","صوت مولّد"],["لغة أخرى","دبلجة"]],"note":"خيارك مكتوب<br>في بطاقتك<br><b style=\"color:#D62828\">السؤال الخامس</b>"},
 {"kind":"cards","title":"إن [[سجّلت]] بصوتك","items":[["غرفة فيها أثاث","لا غرفة فارغة","green"],["شبر من فمك","الهاتف قريب","green"],["وضع الطيران","لا إشعارات","green"],["أخطأت؟","أعد الجملة كاملة","amber"]],"warning":"<b style=\"color:#D62828\">أكبر تحسين بأقل تكلفة:</b> ميكروفون مشبك يُثبَّت على الياقة"},
 {"kind":"grid","title":"إن [[ولّدت]] الصوت","cols":4,"items":[["صوت واحد","لكل السلسلة"],["النسخة المشكولة","والأرقام كلمات"],["جرّب جملتين","قبل النص كاملًا"],["جملة جملة","لا النص كله"]]},
 {"kind":"cards","title":"قِس [[المدة]]","items":[["سجّل المدة","بالثواني","green"],["قارنها ببطاقتك","الفرق صغير؟ ممتاز","green"],["أطول بكثير؟","اختصر النص","amber"],["لا تسرّع الصوت","التسريع يشوّهه","red"]],"warning":"<b style=\"color:#D62828\">قبل النشر:</b> تحقق من حق الاستخدام التجاري"}]

def pages():
    out = [(cover(), [])] + [(c, []) for c in CARDS]
    out += [(gear_page(), []), (tools_page(), []), (prompt_page(), []), (example_page(), []), (mistakes_page(), []), check_page(), worksheet()]
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
    doc.set_metadata({'title': 'مسار الفيديو · الوحدة 3: الصوت', 'author': 'منصة مسار'})
    doc.save(OUT, garbage=3, deflate=True); print('✓', OUT, doc.page_count, 'صفحات', sum(len(b) for b in boxes), 'حقلًا')

if __name__ == '__main__':
    main()
