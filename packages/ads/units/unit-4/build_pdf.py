#!/usr/bin/env python3
"""ملف الوحدة 4 من حقيبة الإعلانات (PDF). التشغيل: python packages/ads/units/unit-4/build_pdf.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pdfkit import *

LABEL = 'مسار الإعلانات · الوحدة 4: من الفكرة إلى قائمة اللقطات'
OUT = os.path.join(ROOT, 'resources/ads/ads-unit-4.pdf')
PROD = os.path.join(ROOT, 'productions/ads-unit-4')
IMG = lambda f, st='': f'<img src="file://{PROD}/{f}" style="display:block;width:100%;border-radius:16px;border:2px solid {T["LINE"]};{st}">'
LTR = lambda s, fs=26: f'<div dir="ltr" style="text-align:left;font-family:monospace;font-size:{fs}px;line-height:1.45;background:#fff;border:3px dashed {T["SEC"]};border-radius:18px;padding:14px 22px">{s}</div>'

SHOTS = [  # الإطار، النبضة، ما يُرى، الحجم والحركة، الصوت، المدة
    ('1', 'البداية', 'نافذتان متقابلتان في حي قديم عند الغروب، في كل نافذة جار وحده', 'واسعة · ثابتة', 'موسيقى هادئة', '5 ث'),
    ('2', 'البداية', 'يد تصب القهوة العربية من دلّة في فنجان سَمَر', 'قريبة · ثابتة', 'صوت الصب', '4 ث'),
    ('3', 'التصاعد', 'البخار يصعد من الفنجان ويخرج من النافذة', 'متوسطة · ميل إلى أعلى', '—', '5 ث'),
    ('4', 'الذروة', 'البخار يمتد جسرًا إلى النافذة المقابلة', 'واسعة · حركة جانبية', '—', '6 ث'),
    ('5', 'الذروة', 'الجار يلتفت ويبتسم', 'قريبة · ثابتة', '—', '4 ث'),
    ('6', 'الختام', 'الجاران معًا، وفنجانان', 'متوسطة · اقتراب بطيء', 'المعلّق: «سَمَر تجمع الناس»', '6 ث'),
]
KIT = 'Product lock: a small white Arabic coffee cup (finjan) with no handle, a thin gold rim and one thin gold band. Same shape and colours in every shot.'
P2 = (KIT + '<br><br>Close-up. A man\'s hand pours light golden Arabic coffee from a brass dallah into the finjan, '
      'on the stone sill of an old Arabian window, golden hour side light, 50mm lens, shallow depth of field, static camera. '
      'No text, no logos, no extra objects.')
P4 = (KIT + '<br><br>Wide shot. Steam rises from the finjan on the window sill and stretches across a narrow old Arabian alley '
      'like a soft curved bridge to the opposite arched window, where a middle-aged man in a white thobe and ghutra looks out. '
      'Sunset haze, 24mm lens, slow sideways camera move. No text, no logos.')

def pages():
    p = [cover('الوحدة 4 · من الفكرة إلى قائمة اللقطات', 'من الفكرة إلى [[قائمة]]',
               ['تقسم الفكرة إلى أربع نبضات.', 'ترسم لوحة قصة من ستة إطارات.', 'تكتب قائمة لقطات مجموع مددها يساوي طول الإعلان.', 'تجمع عُدّة ثبات، وتكتب وصفَي توليد لأهم لقطتين.'],
               'لوحة قصة<br>وقائمة لقطات<br>وعُدّة ثبات')]
    p.append({'kind': 'tree', 'title': 'النبضات [[الأربع]]',
        'rows': [['① البداية', 'تعرّف المكان والناس'], ['② التصاعد', 'يحرّك شيئًا'], ['③ الذروة', 'يظهر فيها الرمز'], ['④ الختام', 'تُقال فيه الرسالة']],
        'note': '<b style="color:#B0186A">الفكرة جملة واحدة</b><br>والإعلان زمن يمضي.<br><br>ضع رمز الفكرة<br>في الذروة، لا في<br>البداية ولا في الختام.'})
    lst = ''.join(f'<div style="font-size:29px;line-height:1.45;margin-bottom:10px"><b style="color:{T["ACC"]}">{n} · {b}:</b> {w}</div>' for n, b, w, *_ in SHOTS)
    p.append(H1('مثال [[مكتمل]]: لوحة قصة «سَمَر»') + f'''<div style="position:absolute;top:280px;right:110px;left:110px;display:flex;gap:36px">
<div style="flex:1.45">{IMG('samar-storyboard-v2.jpg')}<div style="font-size:26px;color:{T['MUT']};margin-top:10px">رسم بالقلم، بلا كلمات ولا شعارات. اللوحة لا تحتاج أن تكون جميلة… تحتاج أن تكون واضحة.</div></div>
<div style="flex:1">{lst}</div></div>''')
    rows = [[f'<b>{n}</b>', b, w, s, a, f'<b>{d}</b>'] for n, b, w, s, a, d in SHOTS]
    p.append(table_page('قائمة لقطات «سَمَر»: سطر لكل [[إطار]]', ['#', 'النبضة', 'ما يُرى', 'الحجم والحركة', 'ما يُسمع', 'المدة'], rows,
        ['5%', '11%', '38%', '18%', '18%', '10%'], 27, '<b>المجموع:</b> 5 + 4 + 5 + 6 + 4 + 6 = <b>30 ثانية</b> = طول الإعلان. الرسالة بالصوت في الختام، لا مكتوبة في الصورة.', top=270))
    water = [['1', 'صنبور مفتوح والفرشاة في الفم', 'متوسطة · ثابتة', 'صوت الماء', '4 ث'], ['2', 'الماء يتحول نقودًا معدنية', 'قريبة · ثابتة', 'رنين النقود', '4 ث'],
             ['3', 'النقود تتكدس في الحوض', 'واسعة · ميل إلى أسفل', '—', '4 ث'], ['4', 'يد تغلق الصنبور', 'قريبة · ثابتة', 'المعلّق: «كل ثانية تُحسب… مالًا»', '3 ث']]
    p.append(table_page('مثال ثانٍ: إعلان [[الماء]] في 15 ثانية', ['#', 'ما يُرى', 'الحجم والحركة', 'ما يُسمع', 'المدة'], water,
        ['6%', '40%', '20%', '24%', '10%'], 30, '<b>الرمز:</b> النقود في الحوض = الهدر (من الوحدة 3)، وظهر في الذروة: اللقطتان 2 و3 · <b>المجموع:</b> 4 + 4 + 4 + 3 = 15 ثانية.', top=290))
    parts = [['من', 'a man\'s hand · the finjan'], ['يفعل ماذا', 'pours coffee'], ['أين', 'old Arabian window sill'], ['الضوء', 'golden hour side light'],
             ['العدسة والحجم', 'close-up · 50mm'], ['حركة الكاميرا', 'static camera'], ['الممنوع', 'no text, no logos, no extra objects']]
    p.append(H1('الوصف: سبعة [[أجزاء]] لكل لقطة') + f'''<div style="position:absolute;top:270px;right:110px;left:110px;display:flex;gap:34px">
<div style="flex:0.85">{table(['الجزء', 'من الإطار 2'], [[f'<b>{a}</b>', f'<span dir="ltr">{b}</span>'] for a, b in parts], ['38%', '62%'], 27, 28)}
<div style="font-size:26px;color:{T['MUT']};margin-top:10px">الوصف بالإنجليزية لأن أدوات التوليد تفهمه أدق. اكتب وصفين لأهم لقطتين الآن، والبقية في الوحدة 5 عند التوليد.</div></div>
<div style="flex:1.15"><div style="font-size:30px;font-weight:700;color:{T['ACC']}">الإطار 2: الصب</div>{LTR(P2, 23)}
<div style="font-size:30px;font-weight:700;color:{T['ACC']};margin-top:14px">الإطار 4: الجسر (الذروة)</div>{LTR(P4, 23)}</div></div>''')
    p.append(H1('عُدّة [[الثبات]]: لأن المولّد لا يتذكر') + f'''<div style="position:absolute;top:270px;right:110px;left:110px;display:flex;gap:30px">
<div style="flex:1"><div style="font-size:32px;font-weight:700;color:{T['GRN']}">المرجع A</div>{IMG('finjan-A.jpg')}</div>
<div style="flex:1"><div style="font-size:32px;font-weight:700;color:{T['ACC']}">بلا عُدّة: تغيّر ✗</div>{IMG('finjan-B.jpg')}</div>
<div style="flex:1"><div style="font-size:32px;font-weight:700;color:{T['GRN']}">بعُدّة: الفنجان نفسه ✓</div>{IMG('finjan-C.jpg')}</div></div>
<div style="position:absolute;top:620px;right:110px;left:110px;{BOX};padding:18px 30px;font-size:30px;line-height:1.55">
<b>العُدّة ثلاثة أشياء:</b> ① صورة مرجعية للمنتج تُرفع مع كل وصف · ② صورة مرجعية لكل شخصية · ③ كتلة وصف ثابتة تُلصق أول كل وصف كما هي، ومعها ضوء وألوان ثابتة للإعلان كله.<br>
<b>من إنتاجنا:</b> B وُلّد بلا مرجع فتغيّر لونه ونقشه، وC وُلّد بالمرجع A فبقي هو نفسه. وملامح سراج نفسه تغيّرت في الوحدة 0، حتى ثبّتناها بقفل الهوية وصورتين مرجعيتين.</div>''')
    p.append(blocks_page('ميزانية [[الزمن]]: اجمع المدد', [
        ('إعلان 15 ثانية', '3 إلى 4 لقطات. لقطة واحدة للرمز على الأقل.'),
        ('إعلان 30 ثانية', '5 إلى 7 لقطات، نحو 5 ثوانٍ للقطة.'),
        ('مقطع المولّد', 'غالبًا 8 ثوانٍ، وتستعمل منه أفضل 3 إلى 6 ثوانٍ فقط.'),
        ('من إنتاجنا', 'آخر جزء من الثانية في مقاطع Flow جاءنا مشوهًا، فلا نستعمله. اترك هامشًا في كل لقطة.'),
        ('زاد المجموع؟', 'احذف لقطة كاملة، ولا تقصّ كل اللقطات قليلًا.'),
        ('لا تُسرع بالكلام', 'نص المعلّق المسموع نحو كلمتين في الثانية. إن لم يتسع النص فاختصره.')], fs=31))
    p.append(prompt_page('''أنت مخرج إعلانات دقيق. هذه فكرة إعلاني ورمزها: [الصق الفكرة والرمز]. طول الإعلان: [15 أو 30] ثانية.
وهذه إطاراتي الستة كما رسمتها: [صف كل إطار في سطر].
1. حوّلها إلى قائمة لقطات بالأعمدة: الرقم، الحجم، حركة الكاميرا، ما يُرى، ما يُسمع، المدة.
2. لا تضف إطارات ولا تغيّر الفكرة. إن رأيت إطارًا زائدًا أو ناقصًا فاقترح ذلك منفصلًا.
3. اجمع المدد، ونبّهني إن زاد المجموع على طول الإعلان، وقل أي لقطة تُحذف.
4. اكتب بالإنجليزية وصف توليد لأهم لقطتين، بالأجزاء السبعة: من، ماذا يفعل، أين، الضوء، العدسة والحجم، حركة الكاميرا، الممنوع.
لا تجاملني: إن كانت الذروة لا تُظهر الرمز فقل ذلك.''',
        'ارسم واكتب بنفسك أولًا، ثم استعمل البرومبت وقارن. يعمل في النسخ المجانية من ChatGPT أو Gemini أو Claude. الأداة رأي ثانٍ، والقرار لك.', fs=31))
    p.append(blocks_page('ليس عندك فكرة فائزة؟ تدرّب على [[«سنابل»]]', [
        ('الموجز', 'مخبز «سنابل» افتُتح في حيّك، ويريد أن يجرّبه السكان هذا الأسبوع.'),
        ('الرسالة', 'سنابل… خبز الحي كل صباح.'),
        ('الفكرة الفائزة للتدريب', 'رغيف ساخن يُكسر نصفين بين جارين لا يعرف أحدهما الآخر.'),
        ('الرمز', 'الرغيف المكسور نصفين = المشاركة بين الجيران.'),
        ('طول الإعلان', '15 ثانية: 3 إلى 4 لقطات.'),
        ('مهمتك', 'املأ أوراق العمل الثلاث في آخر الملف لهذه الفكرة: اللوحة، والقائمة، والعُدّة والوصفين.')]))
    p.append(mistakes_page([
        ('تبدأ التوليد قبل اللوحة', 'لقطات جميلة متفرقة لا تصنع قصة.', 'ارسم الإطارات الستة أولًا.'),
        ('ذروة بلا رمز', 'الإعلان يمرّ ولا يبقى منه شيء.', 'ضع الرمز في النبضة الثالثة.'),
        ('قائمة بلا مدد', 'الإعلان يطول، فتقصّ في آخر لحظة.', 'اجمع المدد قبل أي توليد.'),
        ('وصف عام: «رجل يشرب قهوة»', 'المولّد يخترع كل ما لم تكتبه.', 'الأجزاء السبعة في كل وصف.'),
        ('لا عُدّة ثبات', 'الفنجان يتغيّر بين لقطة وأخرى.', 'صورة مرجعية وكتلة ثابتة.')], fs=32))
    p.append(check_page('قبل أن تنتقل إلى [[الوحدة 5]]', ['قسمت فكرتي إلى أربع نبضات، والرمز في الذروة', 'رسمت ستة إطارات، ولو بالأعواد والدوائر',
        'عرضت الإطارات على شخص بلا كلام، وكتبت ماذا فهم', 'كتبت قائمة اللقطات، ومجموع المدد = طول الإعلان', 'جمعت عُدّة الثبات: صورة للمنتج، وصورة للشخصية، وكتلة ثابتة',
        'كتبت وصفَي توليد لأهم لقطتين بالأجزاء السبعة'], 42))
    # ورقة العمل 1: لوحة القصة
    box = lambda n: f'''<div style="border:3px solid {T['INK']};border-radius:14px;background:#fff;padding:8px 14px">
<div style="font-family:Tajawal;font-size:24px;color:{T['MUT']}">الإطار {n}</div><div style="height:135px"></div>
<div style="font-size:24px">ما يُرى: {fx(380, 36)}</div><div style="font-size:24px">المدة: {fx(120, 36)} ث</div></div>'''
    p.append(H1('ورقة العمل 1: لوحة [[القصة]]') + name_line(275) + f'''<div style="position:absolute;top:345px;right:110px;left:110px">
<div style="font-size:28px;margin-bottom:10px">فكرتي ورمزها: {fx(1400, 40)}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">{''.join(box(i) for i in range(1, 7))}</div>
<div style="font-size:24px;color:{T['MUT']};margin-top:8px">اطبع الورقة وارسم في المربعات بالقلم، أو ارسم على ورقة منفصلة واكتب هنا. الرمز في الذروة: الإطار 4 أو 5 غالبًا.</div></div>''')
    head = ['#', 'الحجم', 'حركة الكاميرا', 'ما يُرى', 'ما يُسمع', 'المدة']
    rows = [[f'<b>{i}</b>', cell(50), cell(50), cell(50), cell(50), cell(50)] for i in range(1, 7)]
    p.append(H1('ورقة العمل 2: قائمة [[اللقطات]]') + name_line(275) + f'''<div style="position:absolute;top:345px;right:110px;left:110px">
{table(head, rows, ['5%', '13%', '17%', '35%', '20%', '10%'], 26, 28)}
<div style="font-size:30px;margin-top:14px">طول الإعلان: {fx(150, 44)} ث &nbsp;&nbsp; مجموع المدد: {fx(150, 44)} ث &nbsp;&nbsp; {fc(34)}متساويان &nbsp; {fc(34)}حذفت لقطة: {fx(300, 44)}</div></div>''')
    p.append(H1('ورقة العمل 3: العُدّة و[[الوصفان]]') + name_line(275) + f'''<div style="position:absolute;top:345px;right:110px;left:110px;font-size:28px;line-height:1.55">
<div style="display:flex;gap:30px"><div style="flex:1">المنتج كما يجب أن يبقى (الشكل واللون): {fx(330, 40)}<br>{fc(32)}عندي صورة مرجعية للمنتج</div>
<div style="flex:1">الشخصية كما يجب أن تبقى: {fx(450, 40)}<br>{fc(32)}عندي صورة مرجعية للشخصية</div></div>
<div style="margin-top:8px">كتلة الوصف الثابتة (بالإنجليزية، تُلصق أول كل وصف):</div><div style="border:2px solid {T['LINE']};border-radius:12px;background:#fff">{cell(70)}</div>
<div style="display:flex;gap:30px;margin-top:10px"><div style="flex:1">وصف اللقطة رقم {fx(70, 40)}:<div style="border:2px solid {T['LINE']};border-radius:12px;background:#fff">{cell(130)}</div></div>
<div style="flex:1">وصف اللقطة رقم {fx(70, 40)}:<div style="border:2px solid {T['LINE']};border-radius:12px;background:#fff">{cell(130)}</div></div></div>
<div style="margin-top:8px;font-size:26px">في الوصفين: {' '.join(fc(28) + x for x in ['من', 'يفعل ماذا', 'أين', 'الضوء', 'العدسة', 'الحركة', 'الممنوع'])}</div></div>''')
    p.append(tangible_page('لوحة قصة «سَمَر» بستة إطارات مرسومة بالقلم، وقائمة لقطاتها بثلاثين ثانية، وعُدّة ثبات للفنجان. <b>وفي فيديو الوحدة ترى الإطارات معروضة واحدًا بعد الآخر بتوقيت الإعلان.</b>',
        'ارسم إطاراتك الستة بالقلم على ورقة: الأعواد والدوائر تكفي. ثم صوّرها بهاتفك، واعرضها واحدًا بعد الآخر بتوقيت قائمتك. اكتب ما تغيّر بعد التجربة:',
        'اعرض الإطارات على شخص بلا كلام، واسأله: «ماذا يحدث؟» إن لم يصل إلى الرمز والرسالة فأعد رسم الذروة.',
        'اللوحة والقائمة والعُدّة والوصفان تدخل التوليد في الوحدة 5.'))
    return p

if __name__ == '__main__':
    build(pages(), LABEL, OUT, 'مسار الإعلانات · الوحدة 4: من الفكرة إلى قائمة اللقطات')
