"""إضافة حقول قابلة للتعبئة إلى ملفات الحقيبة المجانية (طبقة فوق الملف الأصلي، دون تغيير محتواه)."""
import pymupdf,sys,os
R=pymupdf.Rect
def glyphs(p,chars):
    out=[]
    for b in p.get_text('rawdict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                for c in s['chars']:
                    if c['c'] in chars: out.append(R(c['bbox']))
    return out
def thin_lines(p):
    L=[]
    for g in p.get_drawings():
        for it in g['items']:
            if it[0]=='re' and it[1].height<1.5 and it[1].width>25: L.append(R(it[1]))
    return L
class F:
    def __init__(s,doc): s.doc=doc;s.n=0
    def text(s,page,rect,multi=False,size=10):
        w=pymupdf.Widget();s.n+=1;w.field_name=f'p{page.number+1}_t{s.n}'
        w.field_type=pymupdf.PDF_WIDGET_TYPE_TEXT;w.rect=rect;w.text_font='Helv';w.text_fontsize=0 if multi else size
        w.border_width=0;w.fill_color=None
        if multi: w.field_flags|=pymupdf.PDF_TX_FIELD_IS_MULTILINE
        a=page.add_widget(w); s.doc.xref_set_key(a.xref,'Q','2')  # محاذاة لليمين
    def check(s,page,rect):
        w=pymupdf.Widget();s.n+=1;w.field_name=f'p{page.number+1}_c{s.n}'
        w.field_type=pymupdf.PDF_WIDGET_TYPE_CHECKBOX;w.rect=rect;w.border_width=0;w.fill_color=None
        page.add_widget(w)
def workbook(doc,f):
    for p in doc:
        pn=p.number
        for r in thin_lines(p):
            if r.width>505: continue                      # فواصل عرض الصفحة (الرأس والتذييل)
            if pn==2 and 260<r.y0<540: continue           # جدول المقارنة: خلايا لا أسطر
            if pn==4 and 230<r.y0<640: continue           # جدول النسخ وقائمة التحقق
            f.text(p,R(r.x0+2,r.y0-15,r.x1-2,r.y0-1))
        for g in glyphs(p,'☐○'):
            c=g.tl+ (g.br-g.tl)/2; h=max(g.width,g.height)/2+1; f.check(p,R(c.x-h,c.y-h,c.x+h,c.y+h))
        if pn==2:  # درجات الأداتين في جدول المقارنة، والمجموع
            ys=[267.8,315.0,363.0,410.2,458.2,505.5,533.2]
            for a,b in zip(ys,ys[1:]):
                for x0,x1 in ((104.8,167.0),(42.5,104.8)): f.text(p,R(x0+6,a+5,x1-6,b-5),size=14)
        if pn==4:  # جدول سجل النسخ الصغيرة: ثلاث نسخ × ثلاثة أعمدة
            ys=[234.8,282.0,330.0,378.0]
            for a,b in zip(ys,ys[1:]):
                for x0,x1 in ((379.3,512.0),(170.0,379.3),(42.5,170.0)): f.text(p,R(x0+4,a+3,x1-4,b-3),multi=True)
BOX={'قالب صياغة المهمة':R(84,402,876,456),'قالب هندسة التعليمات':R(84,264,876,332)}
def units(doc,f):
    for p in doc:
        for g in p.get_drawings():
            r=g['rect']
            if 20<r.width<24 and abs(r.width-r.height)<1 and g['type']=='fs': f.check(p,R(r.x0+2,r.y0+2,r.x1-2,r.y1-2))
        for k,r in BOX.items():
            if p.search_for(k): f.text(p,r,multi=True)
def run(src,dst):
    doc=pymupdf.open(src);f=F(doc)
    (workbook if 'workbook' in src else units)(doc,f)
    doc.save(dst,garbage=3,deflate=True);print(os.path.basename(dst),doc.page_count,'صفحات',f.n,'حقلًا')
if __name__=='__main__':
    for n in sys.argv[2:]: run(os.path.join(sys.argv[1],n+'.pdf'),os.path.join('out',n+'.pdf'))
