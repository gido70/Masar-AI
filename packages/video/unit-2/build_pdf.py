#!/usr/bin/env python3
"""يبني ملف الوحدة 2 (PDF) بنفس تصميم بطاقات المصنع. التشغيل: python packages/video/unit-2/build_pdf.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, os.path.join(ROOT, 'studio'))
import make_video as M
from playwright.sync_api import sync_playwright
import pymupdf

T = M.THEMES['video']; LABEL = 'مسار الفيديو · الوحدة 2: النص'
OUT = os.path.join(ROOT, 'resources/video/video-unit-2.pdf')
E = lambda s: M.em(s, T)
H1 = lambda t: f'<h1 style="position:absolute;top:150px;right:110px">{E(t)}</h1>'
BOX = f'background:{T["PAPER"]};border:3px solid {T["LINE"]};border-radius:24px'

def compare(c):
    def side(s, col):
        return f'''<div style="flex:1;border:5px solid {col};border-radius:28px;background:#fff;padding:30px 40px">
<div style="display:inline-block;background:{col};color:#fff;font-family:Tajawal;font-size:38px;border-radius:14px;padding:6px 26px">{s['label']}</div>
<div class="rv" style="font-size:50px;line-height:1.5;margin-top:22px;min-height:300px">«{s['text']}»</div>
<div class="rv" style="font-size:44px;font-weight:700;color:{col};border-top:3px solid {T['LINE']};padding-top:16px">{s['verdict']}</div></div>'''
    return H1(c['title']) + f'<div style="position:absolute;top:340px;right:110px;left:110px;display:flex;gap:40px">{side(c["before"],T["ACC"])}{side(c["after"],T["GRN"])}</div>'

def cover():
    goals = ''.join(f'<li style="margin-bottom:10px">{g}</li>' for g in [
        'تكتب نصًا يُفهم من سماعه مرة واحدة.', 'تحسب طول النص من مدة الفيديو.',
        'تقسّم النص إلى جدول مشاهد: ما يُقال وما يظهر والمدة.', 'تشكّل نسخة الصوت فتنطقها الأداة صحيحًا.'])
    return f'''<div style="position:absolute;top:190px;right:110px;left:110px">
<div style="display:inline-block;background:{T['ACC']};color:#fff;font-family:Tajawal;font-size:44px;border-radius:16px;padding:8px 30px">الوحدة 2 · النص</div>
<div style="font-size:150px;font-weight:700;line-height:1.1;margin-top:20px">{E('اكتب [[للأذن]]')}</div>
<div style="display:flex;gap:40px;margin-top:40px">
<div style="flex:1.2;{BOX};padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">ستكون قادرًا على</div><ol style="font-size:44px;line-height:1.45;margin:14px 0 0;padding-right:50px">{goals}</ol></div>
<div style="flex:1;border:4px solid {T['GRN']};border-radius:24px;padding:26px 40px"><div style="font-family:Tajawal;font-size:36px;color:{T['MUT']}">تخرج من الوحدة بـ</div>
<div style="font-size:46px;line-height:1.6;margin-top:14px;font-weight:700;color:{T['GRN']}">نص مشكول للصوت<br>نسخة للترجمة<br>جدول المشاهد</div></div></div></div>'''

PROMPT = '''أنت كاتب نصوص فيديو. هذه بطاقة الفيديو الخاصة بي: [الصق بطاقتك من الوحدة 1]
اكتب نص الفيديو بهذه الشروط:
1. عدد الكلمات = مدة الفيديو بالثواني × 1.8.
2. كل جملة اثنتا عشرة كلمة أو أقل، وفكرة واحدة لكل جملة.
3. ابدأ بما يهم الجمهور، بلا مقدمات.
4. اكتب الأرقام كلمات كما تُنطق.
ثم أعطني أربعة أشياء:
أ. جدول المشاهد: رقم المشهد، وما يُقال، وما يظهر، والمدة. لا يظهر على الشاشة إلا ما يقوله الصوت.
ب. نسخة الصوت مشكولة: شكّل أول الكلمة التي قد تُقرأ خطأ، وسكّن آخر كلمة قبل الوقفة، ولا تشكّل الكلمات الدخيلة مثل فيديو.
ج. نسخة الترجمة بلا تشكيل، بأسطر قصيرة.
د. أصعب جملتين في النطق، لأجربهما بالصوت أولًا.'''

def prompt_page():
    lines = PROMPT.replace('\n', '<br>')
    return H1('برومبت [[جاهز]]') + f'''<div style="position:absolute;top:290px;right:110px;left:110px;border:4px dashed {T['SEC']};border-radius:26px;background:#fff;padding:26px 40px;font-size:33px;line-height:1.5">{lines}</div>
<div style="position:absolute;bottom:100px;left:110px;font-family:Tajawal;font-size:28px;color:{T['MUT']}">انسخه والصقه في Claude أو ChatGPT، ثم راجع الناتج بقائمة التحقق.</div>'''

def table(head, rows, widths, fs=38):
    th = ''.join(f'<th style="width:{w};background:{T["INK"]};color:#fff;font-family:Tajawal;font-size:32px;padding:14px 18px;text-align:right">{h}</th>' for h, w in zip(head, widths))
    tr = ''.join('<tr>' + ''.join(f'<td style="border:2px solid {T["LINE"]};padding:12px 18px;font-size:{fs}px;line-height:1.4;vertical-align:top">{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table style="width:100%;border-collapse:collapse;background:#fff"><tr>{th}</tr>{tr}</table>'

def example_page():
    rows = [['1', 'تريدُ فيديو لمشروعِك، لكنْ لا تعرفُ من أين تبدأْ؟', 'السؤال بخط كبير', '7'],
            ['2', 'في ستِّ خطواتٍ تصنعُه بنفسِك: البطاقة، والنصّ، والصوت، والصورة، والمونتاج، والنشرْ.', 'الخطوات الست، كل خطوة لحظة ذكرها', '10'],
            ['3', 'بالذكاء الاصطناعي، وبتكلفةٍ تعرفُها قبلَ أن تضغطَ أيَّ زرّْ.', 'بطاقة «تكلفة تعرفها مسبقًا»', '8'],
            ['4', 'مسارُ الفيديو: أوّلُ فيديو لك جاهزٌ في نهايةِ الحقيبة. سجِّلِ الآنْ.', 'الشعار وزر التسجيل', '5']]
    return H1('مثال [[مكتمل]]: إعلان 30 ثانية') + f'''<div style="position:absolute;top:320px;right:110px;left:110px">{table(['#','ما يُقال (نسخة الصوت)','ما يظهر','ث'], rows, ['5%','55%','32%','8%'], 37)}
<div style="margin-top:22px;{BOX};padding:18px 30px;font-size:34px;line-height:1.5">40 كلمة لا 55: قائمة الخطوات تُقرأ أبطأ، والشعار يحتاج وقفة. وكُتبت «أوّل فيديو لك» بدل «فيديوك»، لأن أدوات الصوت قد تخطئ في نطقها.</div></div>'''

def mistakes_page():
    items = [('تُظهر العناصر قبل ذكرها', 'يقرأ المشاهد ما لم يُقل بعد فيتشتت، وقد تضطر إلى إعادة الفيديو.', 'اجعل كل عنصر يظهر لحظة ذكره.'),
             ('تترك كلمة تحتمل قراءتين', 'قد تقرأ الأداة «المُدّة» «المَدّة».', 'شكّل الحرف الأول.'),
             ('تكرر التوليد لكلمة أخطأت فيها الأداة', 'كل محاولة تُحسب، وقد يتكرر الخطأ.', 'بعد خطأين، غيّر الكلمة بمرادف.'),
             ('تشكّل الكلمات الدخيلة', 'قد تشدّد الأداة على «فيديو» و«كاميرا» فتبدوان غريبتين.', 'اتركها بلا تشكيل.'),
             ('تقدّر المدة بالإحساس', 'يخرج الفيديو أقصر أو أطول مما خططت.', 'احسب الثواني × 1.8، ثم قِس جملتين بصوتك.')]
    rows = [[f'<b>{a}</b>', b, f'<b style="color:{T["GRN"]}">{c}</b>'] for a, b, c in items]
    return H1('أخطاء [[شائعة]]… وكيف تتجنبها') + f'<div style="position:absolute;top:320px;right:110px;left:110px">{table(["الخطأ","ماذا يحدث","كيف تتجنبه"], rows, ["28%","42%","30%"], 36)}</div>'

def check_page():
    items = ['كل جملة اثنتا عشرة كلمة أو أقل', 'عدد الكلمات = الثواني × 1.8 (بفارق لا يزيد عن 10٪)', 'كل عنصر على الشاشة يذكره الصوت',
             'الأرقام مكتوبة كلمات', 'جرّبت أصعب جملتين بالصوت', 'حفظت النسختين وجدول المشاهد في ملف الإنجاز']
    li = ''.join(f'<div style="display:flex;align-items:center;gap:24px;margin-bottom:22px;font-size:50px"><span style="width:52px;height:52px;border:4px solid {T["INK"]};border-radius:10px;flex:none"></span>{x}</div>' for x in items)
    return H1('قبل أن تنتقل إلى [[الوحدة 3]]') + f'<div style="position:absolute;top:330px;right:130px">{li}</div>'

def worksheet():
    line = f'border-bottom:3px dotted {T["MUT"]};display:inline-block'
    rows = [[str(i), '', '', ''] for i in range(1, 6)]
    t = table(['#', 'ما يُقال (نسخة الصوت، مشكولة)', 'ما يظهر على الشاشة', 'المدة (ث)'], rows, ['5%', '52%', '30%', '13%'], 30)
    return H1('ورقة العمل: [[جدول]] مشاهدك') + f'''<div style="position:absolute;top:290px;right:110px;font-size:36px">الاسم: <span style="{line};width:360px"></span>&nbsp;&nbsp; التاريخ: <span style="{line};width:200px"></span></div>
<div style="position:absolute;top:350px;right:110px;left:110px">
<div style="font-size:40px;margin-bottom:18px">مدة فيديوك (من بطاقتك): <span style="{line};width:120px"></span> ثانية × 1.8 = <span style="{line};width:120px"></span> كلمة</div>{t}
<div style="margin-top:18px;font-size:36px;line-height:1.7">جملتا الاختبار: ① <span style="{line};width:640px"></span> ② <span style="{line};width:640px"></span><br>
☐ نسخة الصوت مشكولة &nbsp;&nbsp; ☐ نسخة الترجمة بلا تشكيل &nbsp;&nbsp; ☐ الكلمات ضمن العدد المحسوب</div></div>'''

CARDS = [
    {'kind': 'compare', 'title': '[[قبل]] وبعد',
     'before': {'label': 'قبل', 'text': 'نقدّم لكم دورة متميزة في صناعة المحتوى باستخدام أحدث التقنيات لتطوير مهاراتكم وتحقيق أهدافكم', 'verdict': 'طويلة · عامة · لا تقول شيئًا'},
     'after': {'label': 'بعد', 'text': 'تريد فيديو لمشروعك؟ في ست خطوات تصنعه بنفسك.', 'verdict': 'قصيرة · واضحة · تخاطبك'}},
    {'kind': 'grid', 'title': 'أربع [[قواعد]] للنص المسموع', 'cols': 4,
     'items': [['جملة قصيرة', '12 كلمة أو أقل'], ['فكرة واحدة', 'لكل جملة'], ['ابدأ بالمهم', 'ما يهمّ المشاهد أولًا'], ['الأرقام كلمات', '«مئة وعشر» لا 110']]},
    {'kind': 'rule_bars', 'title': 'احسب [[طول]] نصك',
     'rule': {'big': '<span dir="ltr">1.8 ×</span>', 'text': '<b>الثواني × 1.8 = عدد الكلمات</b>', 'note': 'من بطاقتك'},
     'bars': [['إعلان', '30 ث ← 55 كلمة', 0.17], ['محتوى قصير', '60 ث ← 110 كلمات', 0.33], ['تعريف بجهة', '90 ث ← 165 كلمة', 0.5], ['درس', '3 د ← 330 كلمة', 0.88]]},
    {'kind': 'tree', 'title': '[[جدول]] المشاهد', 'rows': [['ما يُقال', 'النص المشكول'], ['ما يظهر', 'بطاقة أو لقطة'], ['المدة', 'بالثواني']],
     'note': '<b style="color:#D62828">أشيع خطأ:</b><br>أن تسبق الشاشة الصوت،<br>فتعيد الفيديو كله'},
    {'kind': 'cards', 'title': 'انطق [[صحيحًا]]',
     'items': [['شكّل أول الكلمة', '«المُدّة» لا «المَدّة»', 'green'], ['سكّن قبل الوقفة', 'آخر كلمة في الجملة', 'green'], ['لا تشكّل الدخيل', 'فيديو، كاميرا', 'amber'], ['أخطأ مرتين؟', 'غيّر الكلمة', 'red']],
     'warning': '<b style="color:#D62828">تنبيه:</b> جرّب جملتين قبل توليد النص كاملًا.'},
]

def pages():
    out = [cover()]
    for c in CARDS:
        out.append(compare(c) if c['kind'] == 'compare' else c)
    out += [prompt_page(), example_page(), mistakes_page(), check_page(), worksheet()]
    return out

def main():
    ps = pages(); n = len(ps); work = os.path.join(HERE, '_pdf'); os.makedirs(work, exist_ok=True); parts = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        for i, body in enumerate(ps):
            scene = f'صفحة {i+1} من {n}'
            if isinstance(body, dict):
                html = M.card_html(body, T, LABEL, scene)
            else:
                html = M.frame(T, LABEL, scene, body)
            f = os.path.join(work, f'p{i}.html'); open(f, 'w', encoding='utf-8').write(html)
            pg.goto('file://' + f); pg.wait_for_timeout(300)
            pf = os.path.join(work, f'p{i}.pdf'); pg.pdf(path=pf, width='1920px', height='1080px', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
            parts.append(pf)
        b.close()
    doc = pymupdf.open()
    for pf in parts:
        d = pymupdf.open(pf); doc.insert_pdf(d, from_page=0, to_page=0)
    doc.set_metadata({'title': 'مسار الفيديو · الوحدة 2: النص', 'author': 'منصة مسار'})
    doc.save(OUT, garbage=3, deflate=True); print('✓', OUT, doc.page_count, 'صفحات')

if __name__ == '__main__':
    main()
