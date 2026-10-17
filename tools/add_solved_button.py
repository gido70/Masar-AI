"""يضيف إلى الصفحة الأولى من ملف كراسة مربعًا فيه جملة تعريف وزر «افتح النموذج المحلول» قابل للضغط (17 أكتوبر 2026).
التشغيل: python3 tools/add_solved_button.py <ملف الأصل> <ملف الناتج> <رابط النموذج> x0 y0 x1 y1 [مقياس الخط]"""
import pymupdf, sys, os
src, dst, url = sys.argv[1:4]; x0, y0, x1, y1 = map(float, sys.argv[4:8]); k = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
stack = len(sys.argv) > 9 and sys.argv[9] == 'stack'
FONTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets/fonts')
arch = pymupdf.Archive(FONTS)
css = f"""@font-face {{font-family: Amiri; src: url(Amiri-Regular.ttf);}}
@font-face {{font-family: Amiri; src: url(Amiri-Bold.ttf); font-weight: bold;}}
* {{font-family: Amiri; direction: rtl; text-align: right;}}
p {{margin: 0; font-size: {11*k}px; line-height: 1.5; color: #1F2A37;}}
b {{color: #123E6B;}}"""
doc = pymupdf.open(src); pg = doc[0]
box = pymupdf.Rect(x0, y0, x1, y1)
pg.draw_rect(box, color=(0.79, 0.59, 0.12), fill=(0.98, 0.96, 0.89), width=1.2, radius=0.08)
bw, bh = 150*k, 26*k
btn = pymupdf.Rect(x0 + 10*k, y1 - bh - 9*k, x0 + 10*k + bw, y1 - 9*k) if not stack else pymupdf.Rect(x0 + 10*k, y1 - bh - 9*k, x1 - 10*k, y1 - 9*k)
pg.draw_rect(btn, color=None, fill=(0.07, 0.24, 0.42), radius=0.3)
txt = pymupdf.Rect(btn.x1 + 10*k, y0 + 7*k, x1 - 10*k, y1 - 6*k) if not stack else pymupdf.Rect(x0 + 10*k, y0 + 7*k, x1 - 10*k, btn.y0 - 4*k)
html = '<p><b>قبل أن تبدأ:</b> اطّلع على نموذج محلول يوضح كيف تُعبَّأ الأوراق بمثال واحد متكامل. النموذج يساعدك على الفهم، ولا يغنيك عن تعبئة أوراقك أنت على مهمتك الحقيقية وحسب عملك واحتياجك.</p>'
pg.insert_htmlbox(txt, html, css=css, archive=arch)
pg.insert_htmlbox(btn + (0, 3*k, 0, 0), '<p style="text-align:center;color:#ffffff;font-weight:bold;font-size:%spx">افتح النموذج المحلول</p>' % (12*k), css=css, archive=arch)
pg.insert_link({'kind': pymupdf.LINK_URI, 'from': btn, 'uri': url})
pg.insert_link({'kind': pymupdf.LINK_URI, 'from': box, 'uri': url})
doc.save(dst, garbage=3, deflate=True)
print('✓', dst, 'widgets', sum(len(list(p.widgets())) for p in doc))
