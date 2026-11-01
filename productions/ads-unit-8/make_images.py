"""صور الوحدة 8 (0$): بطاقة الطريقة، والخدمات، وسجل التكلفة، والباقات، والنطاق، وصفحة العرض، والمعرض، والهواتف، والمرفوض."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='../..'; F=f'{R}/studio/fonts/'; A='_assets'; os.makedirs(A, exist_ok=True)
W,H=1920,1080; BG=(246,243,238); INK=(29,29,31); ACC=(176,24,106); GRN=(31,122,77); MUT=(110,105,100)
def f(n,s): return ImageFont.truetype(F+n,s)
def T(d,xy,txt,font,fill=INK,anchor='ra'): d.text(xy,txt,font=font,fill=fill,direction='rtl',language='ar',anchor=anchor)
def canvas(title=None,sub=None):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    if title: T(d,(W-110,70),title,f('Amiri-Bold.ttf',84))
    if sub: T(d,(W-110,190),sub,f('Tajawal-Bold.ttf',34),MUT)
    return im,d
def frame(src,t=None,size=None):
    p='/tmp/_fr.png'
    if src.endswith('.mp4'): subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t or 1),'-i',src,'-frames:v','1',p],check=True); im=Image.open(p).convert('RGB')
    else: im=Image.open(src).convert('RGB')
    if size: im=im.resize(size) if abs(im.width/im.height-size[0]/size[1])<0.02 else cover(im,size)
    return im
def cover(im,size):
    r=max(size[0]/im.width,size[1]/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1))
    x=(im.width-size[0])//2; y=(im.height-size[1])//2; return im.crop((x,y,x+size[0],y+size[1]))
def rr(d,box,fill,outline=None,w=3,r=28): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)

# 1) بطاقة الطريقة
Q=[('0','ماذا أريد أن يفهم المشاهد؟ في جملة واحدة.'),('1','لمن الإعلان؟ وماذا يفعل بعده؟ وما البصيرة: حقيقة يعيشها… لكن…؟'),
   ('2','هل ولّدت عشرين فكرة من القوالب الستة قبل أن أختار؟'),('3','أي فكرة تجتاز بطاقة التقييم؟ وما الصورة الواحدة التي تحملها؟'),
   ('4','ما لوحة القصة بالنبضات الأربع؟ وما الذي يبقى ثابتًا في كل لقطة؟'),('5','هل كل لقطة صالحة بقائمة الفحص؟ وكم كلّفتني فعلًا، ومعها المرفوض؟'),
   ('6','هل تُقال الرسالة مرة واحدة، والموسيقى تحت الكلام، والإفصاح موجود؟'),('7','ما البدايات الثلاث؟ وأيها يختار الناس بالأرقام؟'),('8','ما حدّي الأدنى؟ وما الباقات الثلاث التي أعرضها؟')]
im,d=canvas('بطاقة الطريقة: تسعة أسئلة لأي إعلان')
y=200
for n,q in Q:
    rr(d,(110,y,W-110,y+76),(255,255,255),(225,218,210),2,18)
    d.ellipse((W-200,y+10,W-144,y+66),fill=ACC); d.text((W-172,y+38),n,font=f('Tajawal-Bold.ttf',34),fill='white',anchor='mm')
    T(d,(W-225,y+16),q,f('Tajawal-Bold.ttf',36)); y+=86
T(d,(W-110,y+14),'إن أجبت عن الأسئلة التسعة، فعندك إعلان يُفهم ويُتذكّر ويُباع بقيمته.',f('Amiri-Bold.ttf',40),GRN)
im.save(f'{A}/method-card.png')

# 2) الخدمات (رسم توضيحي محايد)
im,d=canvas('خدمات «إعلان فيديو بالذكاء الاصطناعي»','رصد في خمسات · 1 نوفمبر 2026 · موقع واحد · السعر الابتدائي المعروض لا السعر النهائي')
P=['تبدأ من 5$','تبدأ من 10$','تبدأ من 5$','تبدأ من 15$','تبدأ من 5$','تبدأ من 10$']
for i,p in enumerate(P):
    c=i%3; r=i//3; x0=110+c*580; y0=290+r*360
    rr(d,(x0,y0,x0+540,y0+320),(255,255,255),(225,218,210),2,22)
    d.rounded_rectangle((x0+20,y0+20,x0+520,y0+190),radius=14,fill=(222,216,208)); d.polygon([(x0+250,y0+75),(x0+250,y0+135),(x0+300,y0+105)],fill=(255,255,255))
    T(d,(x0+520,y0+205),'إعلان فيديو بالذكاء الاصطناعي',f('Tajawal-Bold.ttf',30)); T(d,(x0+520,y0+255),p,f('Tajawal-Bold.ttf',36),ACC)
T(d,(W-110,1020),'رسم توضيحي، لا صورة من الموقع، وبلا أسماء بائعين',f('Tajawal-Bold.ttf',24),MUT)
im.save(f'{A}/services.png')

# 3) سجل التكلفة الحقيقي (الوحدة 5)
im,d=canvas('التكلفة الحقيقية لإعلان سَمَر','من سجل الوحدة 5: كل محاولة مدفوعة تُحسب، ومعها المرفوض')
rows=[('1 النافذتان','1','20'),('2 الصب','1','20'),('3 البخار يصعد','3','60'),('4 الجسر','3','60'),('5 الجار يشمّ','2','40'),('6 اللقاء','3','60'),('المجموع','13 محاولة','260 نقطة')]
x=[W-110,W-760,W-1110]; y=290
for j,h in enumerate(['اللقطة','المحاولات','النقاط']): T(d,(x[j],y),h,f('Tajawal-Bold.ttf',36),MUT)
y+=60
for k,rw in enumerate(rows):
    last=k==len(rows)-1; ft=f('Tajawal-Bold.ttf',40 if last else 36)
    if last: d.line((110,y-8,W-110,y-8),fill=INK,width=3)
    for j,v in enumerate(rw): T(d,(x[j],y),v,ft,ACC if last else INK)
    y+=64
rr(d,(110,y+20,W-110,y+130),(255,255,255),GRN,4,22)
T(d,(W-150,y+45),'الحد الأدنى = تكلفة الأدوات + المحاولات المرفوضة + وقتك',f('Amiri-Bold.ttf',48),GRN)
im.save(f'{A}/costlog.png')

# 4) الباقات (4 حالات)
th=[frame(f'{R}/productions/ads-unit-6/samar-ad.mp4',26,(460,259)),None,frame(f'{R}/productions/ads-unit-4/samar-storyboard-v2.jpg',None,(460,259))]
def phones(size=(1920,1080)):
    c=Image.new('RGB',size,BG); dd=ImageDraw.Draw(c); pw,ph=int(size[1]*0.75*9/16),int(size[1]*0.75)
    for i,(n,t) in enumerate([('curiosity',2.5),('contrast',3.2),('empathy',2.5)]):
        fr=frame(f'{R}/productions/ads-unit-7/samar-{n}-9x16.mp4',t,(pw,ph)); x=size[0]//2+int(0.6*pw)-i*int(1.1*pw); y=(size[1]-ph)//2  # يُقرأ من اليمين: الفضول أولًا
        dd.rounded_rectangle((x-10,y-14,x+pw+10,y+ph+14),radius=int(pw*0.12),fill=(25,25,28)); c.paste(fr,(x,y))
    return c
ph3=phones(); ph3.save(f'{A}/phones3.png'); th[1]=cover(ph3.crop((300,0,1620,1080)),(460,259))
PK=[('أساسية','إعلان واحد بمقاس واحد','جولة تعديل واحدة','150 وحدة'),('قياسية','+ 3 نسخ بخطافات + مقاسان','جولتا تعديل','300 وحدة'),('شاملة','+ موجز وبصيرة + 3 أفكار + خطة اختبار','ثلاث جولات تعديل','500 وحدة')]
for k in range(1,5):
    im,d=canvas('ثلاث باقات بحجم العمل','الباقة: عرض بحجم عمل محدد')
    for i,(nm,a,b,pr) in enumerate(PK):
        x0=W-110-(i+1)*560+20; y0=280; on=i<k
        card=Image.new('RGB',(540,640),(255,255,255)); cd=ImageDraw.Draw(card)
        card.paste(th[i],(40,30)); T(cd,(500,310),nm,f('Amiri-Bold.ttf',60),ACC); T(cd,(500,400),a,f('Tajawal-Bold.ttf',30)); T(cd,(500,450),b,f('Tajawal-Bold.ttf',30),MUT); T(cd,(500,530),pr,f('Tajawal-Bold.ttf',46),GRN)
        if not on: card=Image.blend(card,Image.new('RGB',card.size,BG),0.82)
        im.paste(card,(x0,y0)); d.rounded_rectangle((x0,y0,x0+540,y0+640),radius=26,outline=(225,218,210),width=3)
    if k==4:
        rr(d,(110,950,W-110,1040),(255,240,246),ACC,3,20); T(d,(W-140,968),'أرقام للتوضيح فقط · حد أدنى افتراضي 100 وحدة · سعرك يبدأ من حدّك أنت',f('Tajawal-Bold.ttf',36),ACC)
    im.save(f'{A}/packages-{k}.png')

# 5) نطاق العمل
im,d=canvas('نطاق العمل','ما يدخل في السعر، وما لا يدخل… مكتوبًا قبل البدء')
cols=[('يدخل في السعر',GRN,['إعلان 30 ثانية','نسختان بمقاسين','جولتا تعديل']),('لا يدخل',ACC,['لقطات جديدة بعد الموافقة','مقاس ثالث','جولة تعديل ثالثة'])]
for i,(h,c,items) in enumerate(cols):
    x1=W-110-i*870; rr(d,(x1-820,280,x1,900),(255,255,255),c,4,26); T(d,(x1-40,310),h,f('Amiri-Bold.ttf',60),c)
    for j,it in enumerate(items): T(d,(x1-40,450+j*120),it,f('Tajawal-Bold.ttf',44))
im.save(f'{A}/scope.png')

# 6) صفحة العرض (5 حالات: بلا إبراز ثم كل قسم)
S=[('مشكلة العميل','الشباب يجتمعون كل مساء… لكن لا يلتقون'),('فكرتك','جسر من البخار بين نافذتين: سَمَر تجمع الناس'),('ما سيستلمه','الباقة القياسية: إعلان + 3 نسخ + مقاسان'),('الخطوة التالية','موافقتك على الباقة، وموعد البدء')]
for k in range(5):
    im,d=canvas(); im.paste(Image.new('RGB',(W,H),(232,226,218)))
    d=ImageDraw.Draw(im); rr(d,(460,50,1460,1030),(255,255,255),(210,200,190),2,16)
    T(d,(1400,90),'عرض لـ: قهوة سَمَر',f('Amiri-Bold.ttf',54)); T(d,(1400,170),'صفحة واحدة',f('Tajawal-Bold.ttf',28),MUT)
    for i,(h,b) in enumerate(S):
        y0=250+i*190; hi=(i==k-1)
        rr(d,(510,y0,1410,y0+160),(255,240,246) if hi else (250,248,245),ACC if hi else (230,224,216),4 if hi else 2,18)
        T(d,(1380,y0+20),h,f('Amiri-Bold.ttf',44),ACC if hi else INK); T(d,(1380,y0+90),b,f('Tajawal-Bold.ttf',32))
    im.save(f'{A}/proposal-{k}.png')

# 7) المعرض التجريبي
im,d=canvas('معرض تجريبي… مكتوب عليه أنه تجريبي')
G=[frame(f'{R}/productions/ads-unit-6/samar-ad.mp4',26,(800,450)),frame(f'{R}/productions/ads-unit-6/_assets/itqan-end.jpg',None,(800,450)),
   cover(ph3.crop((300,0,1620,1080)),(800,450)),frame(f'{R}/productions/ads-unit-5/samar-s4-bridge-v3.mp4',5,(800,450))]
for i,g in enumerate(G):
    x0=W-110-(i%2+1)*840+40; y0=200+(i//2)*430; im.paste(g.resize((800,390)) if False else cover(g,(800,390)),(x0,y0))
    rr(d,(x0+20,y0+320,x0+560,y0+372),(255,255,255),None,0,12); T(d,(x0+545,y0+326),'تجريبي · مولّد بالذكاء الاصطناعي',f('Tajawal-Bold.ttf',30),ACC)
im.save(f'{A}/portfolio.png')

# 8) المرفوض الحقيقي (الوحدة 5)
im,d=canvas('المرفوض جزء من الطريقة','صور بداية رُفضت فعلًا في الوحدة 5، ومعها تكلفتها')
rj=['samar-s3-start-rejected-1.jpg','samar-s4-start-rejected-1.jpg','samar-s4-start-rejected-2.jpg','samar-s6-start-rejected-1.jpg']
for i,r in enumerate(rj):
    x0=W-110-(i%2+1)*840+40; y0=260+(i//2)*400; g=cover(frame(f'{R}/productions/ads-unit-5/{r}'),(800,370)); im.paste(g,(x0,y0))
    d.line((x0+30,y0+30,x0+130,y0+130),fill=ACC,width=14); d.line((x0+130,y0+30,x0+30,y0+130),fill=ACC,width=14)
im.save(f'{A}/rejected.png')
print('ok')
