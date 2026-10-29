"""يضيف في آخر ملف كراسة CPS صفحة «الكراسة التفاعلية بالأمثلة» بزر قابل للضغط، دون تغيير أي صفحة قائمة (29 أكتوبر 2026).
السبب: CPS لا يقبل ملفًا جديدًا دون أن يغيّر الدرجات، فتُضاف الكراسة التفاعلية داخل الملف نفسه وبالرابط نفسه.
التشغيل: python3 tools/add_workbook_page.py <ملف الأصل> <ملف الناتج> <رابط الكراسة التفاعلية> "<اسم الحقيبة>" "<مثال النموذج المحلول>"
"""
import pymupdf, sys, os
src, dst, url, pkg, example = sys.argv[1:6]
FONTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets/fonts')
arch = pymupdf.Archive(FONTS)
css = """@font-face {font-family: Amiri; src: url(Amiri-Regular.ttf);}
@font-face {font-family: Amiri; src: url(Amiri-Bold.ttf); font-weight: bold;}
* {font-family: Amiri; direction: rtl; text-align: right; color: #1F2A37;}
h1 {font-size: 30px; color: #123E6B; margin: 0 0 6px;} .k {font-size: 15px; color: #B7791F; font-weight: bold; margin: 0;}
p {font-size: 15px; line-height: 1.75; margin: 0 0 10px;} li {font-size: 15px; line-height: 1.75;} b {color: #123E6B;}"""
doc = pymupdf.open(src); n0 = len(doc); W, H = doc[0].rect.width, doc[0].rect.height; s = W / 595
pg = doc.new_page(width=W, height=H)
m = 48 * s
pg.draw_rect(pymupdf.Rect(0, 0, W, 10 * s), color=None, fill=(0.07, 0.24, 0.42))
html = f"""<p class="k">إضافة إلى الكراسة · {pkg}</p><h1>✍️ الكراسة التفاعلية بالأمثلة</h1>
<p>أوراق العمل التي سبقت هذه الصفحة هي كراستك الأساسية، تملؤها أثناء دراسة الوحدات. وهذه نسخة تفاعلية منها على الإنترنت تساعدك على البدء حين لا تعرف ماذا تكتب:</p>
<p>• <b>أمثلة جاهزة</b> بجانب كل خانة، من مجالات مختلفة، تختار منها ثم تعدّلها على مشروعك.</p>
<p>• <b>نموذج محلول كامل</b> يعبئ الأوراق كلها بمثال واحد متكامل: {example}.</p>
<p>• <b>برومبت يتركّب من إجاباتك</b>، تنسخه بضغطة وتلصقه في نموذج الذكاء الاصطناعي ليطبّق معك.</p>
<p>• تحفظ إجاباتك في متصفحك، وتطبعها أو تحفظها PDF متى شئت.</p>
<p>الطريقة مكتوبة لتصلح لأي مثال، لا لمثال الحقيبة وحده: غيّر المثال، واتبع الخطوات نفسها.</p>"""
pg.insert_htmlbox(pymupdf.Rect(m, 60 * s, W - m, 395 * s), html, css=css, archive=arch)
btn = pymupdf.Rect(W / 2 - 150 * s, 400 * s, W / 2 + 150 * s, 446 * s)
pg.draw_rect(btn, color=None, fill=(0.07, 0.24, 0.42), radius=0.3)
pg.insert_htmlbox(btn + (0, 9 * s, 0, 0), '<p style="text-align:center;color:#ffffff;font-weight:bold;font-size:19px">افتح الكراسة التفاعلية</p>', css=css, archive=arch)
pg.insert_link({'kind': pymupdf.LINK_URI, 'from': btn, 'uri': url})
pg.insert_htmlbox(pymupdf.Rect(m, 460 * s, W - m, 500 * s), f'<p style="text-align:center;font-size:12px;color:#5B6675">{url}</p>', css=css, archive=arch)
pg.insert_link({'kind': pymupdf.LINK_URI, 'from': pymupdf.Rect(m, 460 * s, W - m, 490 * s), 'uri': url})
doc.save(dst, garbage=3, deflate=True)
print('✓', dst, f'{n0} → {len(doc)} صفحة')
