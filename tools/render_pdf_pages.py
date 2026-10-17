"""يحوّل صفحات ملفات PDF إلى صور JPEG للعرض داخل المنصة (13 أكتوبر 2026).
السبب: مكتبة pdf.js تفكك الحروف العربية في ملفاتنا، بينما MuPDF يرسمها صحيحة.
التشغيل من جذر المستودع: python3 tools/render_pdf_pages.py   (يحتاج pymupdf وPillow)
المخرج: assets/pdfpages/<اسم الملف>/NN.jpg و assets/pdfpages/index.json
أعد التشغيل كلما تغيّر ملف PDF (يتخطى الملفات التي لم يتغير حجمها وتاريخها)."""
import pymupdf, os, json, glob, io
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets/pdfpages'); os.makedirs(OUT, exist_ok=True)
idx_path = os.path.join(OUT, 'index.json')
idx = json.load(open(idx_path, encoding='utf-8')) if os.path.exists(idx_path) else {}
files = sorted(glob.glob(os.path.join(ROOT, 'resources/*.pdf')) + glob.glob(os.path.join(ROOT, 'resources/video/*.pdf')) + glob.glob(os.path.join(ROOT, 'lectures/*.pdf')) + glob.glob(os.path.join(ROOT, 'resources/cps/*.pdf')))
for f in files:
    rel = os.path.relpath(f, ROOT); st = os.stat(f); sig = f'{st.st_size}'
    stem = rel.replace('resources/', '').replace('/', '_')[:-4]
    if idx.get(rel, {}).get('sig') == sig and os.path.exists(os.path.join(OUT, stem, '01.jpg')): continue
    d = pymupdf.open(f); od = os.path.join(OUT, stem); os.makedirs(od, exist_ok=True)
    for old in glob.glob(os.path.join(od, '*.jpg')): os.remove(old)
    for i, p in enumerate(d):
        z = 1400 / max(p.rect.width, p.rect.height)
        pix = p.get_pixmap(matrix=pymupdf.Matrix(z, z), annots=False)
        Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB').save(os.path.join(od, f'{i+1:02d}.jpg'), quality=82, optimize=True)
    idx[rel] = {'dir': f'assets/pdfpages/{stem}', 'pages': d.page_count, 'sig': sig, 'ratio': round(d[0].rect.height / d[0].rect.width, 4)}
    print('✓', rel, d.page_count)
json.dump(idx, open(idx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
