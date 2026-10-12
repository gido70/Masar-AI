"""حقول قابلة للتعبئة لورقتي العمل في وحدتي الفيديو 1 و2 (طبقة فوق الملف؛ يُشغَّل على الأصل بلا حقول)."""
import pymupdf, sys, importlib.util, os
spec = importlib.util.spec_from_file_location('ff', os.path.join(os.path.dirname(__file__), 'add_free_package_fields.py'))
ff = importlib.util.module_from_spec(spec); spec.loader.exec_module(ff)
R = pymupdf.Rect

def dot_runs(p, minw=20):
    runs = []
    for b in p.get_text('rawdict')['blocks']:
        for l in b.get('lines', []):
            cur = None
            for s in l['spans']:
                for c in s['chars']:
                    r = R(c['bbox'])
                    if c['c'] in '.…·':
                        if cur and abs(r.y0 - cur.y0) < 3 and (r.x0 - cur.x1) < 4 and (cur.x0 - r.x1) < 4: cur |= r
                        else:
                            if cur and cur.width >= minw: runs.append(cur)
                            cur = R(r)
                    else:
                        if cur and cur.width >= minw: runs.append(cur)
                        cur = None
            if cur and cur.width >= minw: runs.append(cur)
    return runs

def shape_dot_runs(p, n=5):
    """أسطر نقطية مرسومة أشكالًا صغيرة (لا نصًا)."""
    from collections import defaultdict
    rows = defaultdict(list)
    for g in p.get_drawings():
        r = g['rect']
        if r.width < 5 and r.height < 5: rows[round(r.y0)].append(r)
    out = []
    for y, xs in rows.items():
        xs.sort(key=lambda r: r.x0); run = [xs[0]]
        for r in xs[1:]:
            if r.x0 - run[-1].x1 > 8:
                if len(run) >= n: out.append(R(run[0].x0, run[0].y0, run[-1].x1, run[-1].y1))
                run = [r]
            else: run.append(r)
        if len(run) >= n: out.append(R(run[0].x0, run[0].y0, run[-1].x1, run[-1].y1))
    return out

def finish(doc, f, dst):
    af = doc.pdf_catalog()
    doc.xref_set_key(af, 'AcroForm/NeedAppearances', 'true'); doc.xref_set_key(af, 'AcroForm/Q', '2'); doc.xref_set_key(af, 'AcroForm/DA', '(0 0 0 rg /Helv 0 Tf)')
    for pg in doc:
        for w in pg.widgets():
            if w.field_type == pymupdf.PDF_WIDGET_TYPE_TEXT: w.update()
    doc.save(dst, garbage=3, deflate=True); print(os.path.basename(dst), f.n, 'حقلًا')

def unit1(src, dst):
    doc = pymupdf.open(src); f = ff.F(doc); p = doc[7]
    for r in ff.thin_lines(p):
        if r.width > 505: continue
        f.text(p, R(r.x0 + 2, r.y0 - 15, r.x1 - 2, r.y0 - 1))
    for r in dot_runs(p): f.text(p, R(r.x0, r.y0 - 3, r.x1, r.y1 + 2), size=9)
    for g in ff.glyphs(p, '☐□▢'):
        c = g.tl + (g.br - g.tl) / 2; h = max(g.width, g.height) / 2 + 1; f.check(p, R(c.x - h, c.y - h, c.x + h, c.y + h))
    finish(doc, f, dst)

def unit2(src, dst):
    doc = pymupdf.open(src); f = ff.F(doc); p = doc[11]
    for r in dot_runs(p): f.text(p, R(r.x0, r.y0 - 4, r.x1, r.y1 + 3), size=14)
    for r in shape_dot_runs(p): f.text(p, R(r.x0, r.y0 - 20, r.x1, r.y1 + 2), size=14)
    ys = [379.5, 429.0, 480.0, 531.0, 582.0, 633.0]
    for a, b in zip(ys, ys[1:]):
        for x0, x1 in ((630.0, 1292.2), (248.2, 630.0), (82.5, 248.2)):
            f.text(p, R(x0 + 5, a + 4, x1 - 5, b - 4), multi=(x1 - x0) > 200, size=16)
    for g in ff.glyphs(p, '☐□▢'):
        c = g.tl + (g.br - g.tl) / 2; h = max(g.width, g.height) / 2 + 2; f.check(p, R(c.x - h, c.y - h, c.x + h, c.y + h))
    finish(doc, f, dst)

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    unit1(os.path.join(src, 'video-unit-1.pdf'), os.path.join(out, 'video-unit-1.pdf'))
    unit2(os.path.join(src, 'video-unit-2.pdf'), os.path.join(out, 'video-unit-2.pdf'))
