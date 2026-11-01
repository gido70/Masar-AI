"""مشاهد الوحدة 8 بالمونتاج (0$): كل مشهد فيديو صامت بطول صوته + ثانية، وكل جزء فوق جملته، وسطر واحد فوق الصورة.
التشغيل: python3 make_scenes.py [اسم_المشهد]"""
import os, sys, subprocess, json
from PIL import Image, ImageDraw, ImageFont
R='../..'; F=f'{R}/studio/fonts/'; A='_assets'; P=f'{R}/productions'; os.makedirs('tmp', exist_ok=True); os.makedirs('scenes', exist_ok=True)
ACC=(176,24,106); INK=(29,29,31)
def sh(*a): subprocess.run(a, check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def cap(name, title, kicker=''):
    im=Image.new('RGBA',(1920,1080),(0,0,0,0)); d=ImageDraw.Draw(im)
    ft=ImageFont.truetype(F+'Amiri-Bold.ttf',62); fk=ImageFont.truetype(F+'Amiri-Bold.ttf',34)
    bt=d.textbbox((0,0),title,font=ft,direction='rtl',language='ar'); w=bt[2]-bt[0]
    bk=d.textbbox((0,0),kicker,font=fk,direction='rtl',language='ar') if kicker else (0,0,0,0)
    W=max(w,bk[2]-bk[0])+90; h=(150 if kicker else 110)
    x1=1920-80; y1=1080-90; x0=x1-W; y0=y1-h
    d.rounded_rectangle((x0,y0,x1,y1),radius=24,fill=(255,255,255,240)); d.rectangle((x1-14,y0,x1,y1),fill=ACC+(255,))
    if kicker: d.text((x1-45,y0+16),kicker,font=fk,fill=ACC,direction='rtl',language='ar',anchor='ra')
    d.text((x1-45,y0+(58 if kicker else 18)),title,font=ft,fill=INK,direction='rtl',language='ar',anchor='ra')
    p=f'tmp/cap-{name}.png'; im.save(p); return p
def piece(out, src, d, ss=0.0, title=None, kicker='', zoom=False):
    img = not src.endswith('.mp4')
    inp = ['-loop','1','-t',f'{d:.3f}','-i',src] if img else ['-ss',f'{ss}','-i',src]
    base='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080'
    if img and src in TEXTY and title:
        base='scale=1440:810,pad=1920:1080:240:20:color=0xF6F3EE'
    elif img and zoom: base=f"scale=2112:1188,zoompan=z='min(1+0.0004*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(d*25)+5}:s=1920x1080:fps=25"
    vf=f"[0:v]{base},fps=25,setsar=1,tpad=stop_mode=clone:stop_duration={d+1:.2f},trim=duration={d:.3f},setpts=PTS-STARTPTS,format=yuv420p"
    if title:
        c=cap(os.path.basename(out)[:-4],title,kicker); inp+=['-loop','1','-t',f'{d:.3f}','-i',c]
        vf+="[v];[1:v]format=rgba,fade=t=in:st=0.1:d=0.3:alpha=1[c];[v][c]overlay=0:0:shortest=1,format=yuv420p"
    sh('ffmpeg','-v','error','-y',*inp,'-filter_complex',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','19','-t',f'{d:.3f}',out)
def scene(name, audio, parts):
    """parts: [(start_time, src, ss, title, kicker)] بداية كل جزء في زمن الصوت؛ آخر جزء حتى طول الصوت + 1.2."""
    T=dur(audio)+1.2; files=[]
    for k,(t0,src,ss,title,kick) in enumerate(parts):
        t1=parts[k+1][0] if k+1<len(parts) else T
        o=f'tmp/{name}-{k}.mp4'; piece(o,src,t1-t0,ss,title,kick); files.append(o)
    lst=f'tmp/{name}.txt'; open(lst,'w').write(''.join(f"file '{os.path.basename(f)}'\n" for f in files))
    sh('ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy',f'scenes/{name}.mp4'); print(name, round(T,2), round(dur(f'scenes/{name}.mp4'),2))

TEXTY=set()
U=lambda n,f: f'{P}/ads-unit-{n}/{f}'
LOOK={0:U(0,'presenter-open.mp4'),1:U(1,'presenter-open.mp4'),2:U(2,'base-open.mp4'),3:U(3,'presenter-open.mp4'),4:U(4,'presenter-open.mp4'),5:U(5,'presenter-open.mp4'),6:U(6,'presenter-open.mp4'),7:U(7,'presenter-open.mp4')}
def fr(src,t,name):
    o=f'tmp/fr-{name}.png'; sh('ffmpeg','-v','error','-y','-ss',str(t),'-i',src,'-frames:v','1',o); return o
STUDY=fr(f'{R}/media/ads-unit-2.mp4',50,'study'); TEMPL=fr(f'{R}/media/ads-unit-2.mp4',70,'templ'); CRIT=fr(f'{R}/media/ads-unit-3.mp4',70,'crit')
AD=U(6,'samar-ad.mp4'); MAJ=U(1,'broll-6-crop.mp4'); BR=U(5,'samar-s4-bridge-v3.mp4'); SB=U(4,'samar-storyboard-v2.jpg'); POUR=U(5,'samar-s2.mp4'); END7=U(7,'ad-ending.mp4')
WB=f'{R}/assets/pdfpages/ads_ads-unit-7/14.jpg'; PDF=f'{R}/assets/pdfpages/ads_ads-unit-7/04.jpg'
TEXTY.update([STUDY,TEMPL,CRIT,WB,PDF]+[f'{A}/{x}.png' for x in ['method-card','costlog','services','phones3','packages-4','rejected','portfolio','scope']])
S={
 'n-2a': [(0,U(0,'broll-1a.mp4'),0.5,'قبل: الأداة وحدها','بداية الحقيبة'),(2.0,U(0,'broll-1b.mp4'),0.5,'قبل: الأداة وحدها','بداية الحقيبة'),(4.1,U(0,'broll-1c.mp4'),0.5,'مبهر… ولا يبقى منه شيء','بداية الحقيبة')],
 'n-2b': [(0,AD,6.0,'بعد: إعلان سَمَر','فكرة · بصيرة · رمز · صوت'),(5.6,AD,13.5,'الأداة نفسها… والطريقة مختلفة','')],
 'n-3':  [(0,AD,24.0,'رحلة سَمَر','من سؤال إلى إعلان'),
          (1.94,LOOK[1],2.0,None,''),(2.9,MAJ,0.3,'نجتمع كل مساء… لكن لا نلتقي','الوحدة 1 · الموجز والبصيرة'),
          (7.78,LOOK[2],2.0,None,''),(8.6,TEMPL,0,'عشرون فكرة من القوالب الستة','الوحدة 2 · محرّك الأفكار'),
          (11.05,LOOK[3],2.0,None,''),(11.9,BR,0.5,'جسر من البخار بين نافذتين','الوحدة 3 · الفكرة والرمز'),
          (17.49,LOOK[4],2.0,None,''),(18.3,SB,0,'لوحة القصة بالنبضات الأربع','الوحدة 4 · اللقطات'),
          (20.36,LOOK[5],2.0,None,''),(21.1,POUR,0.3,'لقطات ثابتة بتكلفتها الحقيقية','الوحدة 5 · التوليد'),
          (23.95,LOOK[6],2.0,None,''),(24.6,END7,0.5,'الصوت والمونتاج','الوحدة 6'),
          (25.71,LOOK[7],2.0,None,''),(26.4,f'{A}/phones3.png',0,'ثلاث نسخ بثلاث بدايات','الوحدة 7 · النسخ')],
 'n-4':  [(0,f'{A}/method-card.png',0,None,''),
          (8.34,LOOK[0],2.0,'ماذا أريد أن يفهم المشاهد؟','الوحدة 0'),(10.75,MAJ,0.5,'لمن الإعلان؟ وما البصيرة؟','الوحدة 1'),
          (13.52,TEMPL,0,'ما الأفكار العشرون؟','الوحدة 2'),(15.27,BR,1.0,'أي فكرة تجتاز البطاقة؟','الوحدة 3'),
          (17.82,SB,0,'ما اللقطات؟','الوحدة 4'),(19.05,f'{A}/costlog.png',0,'كم كلّفت؟','الوحدة 5'),
          (20.43,END7,1.5,'هل تُسمع الرسالة؟','الوحدة 6'),(22.03,f'{A}/phones3.png',0,'أي بداية يختار الناس؟','الوحدة 7'),
          (24.05,f'{A}/packages-4.png',0,'بكم أبيع؟','الوحدة 8'),(25.82,f'{A}/method-card.png',0,None,'')],
 'n-5':  [(0,STUDY,0,'على ماذا بُنيت الطريقة؟',''),(4.55,STUDY,0,'Goldenberg وزملاؤه، 1999 · إعلانات مطبوعة','دراسة محكّمة · الإبداع والتذكر لا المبيعات'),
          (14.45,CRIT,0,'خبرة ممارسين بمصادرها','Made to Stick · وغيرها'),(17.57,f'{A}/rejected.png',0,'إنتاج حقيقي بأخطائه وتكلفته','')],
 'n-6':  [(0,AD,20.0,'ما معك الآن',''),(3.54,AD,26.0,'إعلان كامل',''),(4.83,f'{A}/phones3.png',0,'ثلاث نسخ',''),
          (6.12,WB,0,'كراسة بأمثلة محلولة',''),(8.55,PDF,0,'طريقة لأي منتج','')],
 'n-8':  [(0,f'{A}/services.png',0,None,''),(18.71,f'{A}/phones3.png',0,'أنت تبيع الحل','الموجز · الفكرة · النسخ'),(23.49,f'{A}/costlog.png',0,None,'')],
 'n-9':  [(0,f'{A}/packages-1.png',0,None,''),(6.84,f'{A}/packages-2.png',0,None,''),(9.92,f'{A}/packages-3.png',0,None,''),(14.22,f'{A}/packages-4.png',0,None,'')],
 'n-10': [(0,f'{A}/scope.png',0,None,''),(4.59,f'{A}/proposal-0.png',0,None,''),(6.77,f'{A}/proposal-1.png',0,None,''),(8.07,f'{A}/proposal-2.png',0,None,''),(9.08,f'{A}/proposal-3.png',0,None,''),(10.35,f'{A}/proposal-4.png',0,None,'')],
 'n-11': [(0,AD,30.0,'كن صادقًا مع عميلك',''),(2.23,AD,30.0,'أخبره بالذكاء الاصطناعي','سطر الإفصاح في ختام سَمَر'),(4.36,AD,30.0,'أدوات بخطة تجارية',''),(6.33,AD,30.0,'لا وعود بمبيعات',''),(8.24,f'{A}/portfolio.png',0,None,'')],
}
if __name__=='__main__':
    for n in (sys.argv[1:] or S): scene(n, f'{n}.mp3', S[n])
