import json, os, re, datetime, sys
sys.path.insert(0,'/home/claude/deckgen')
from clean import clean, check, WARN
from shapes_svg import S as SHAPESVG
ROOT='/mnt/user-data/outputs/artifacts/3d0c50db-bed3-4757-9dad-965c9fa6f466/project'
os.makedirs(ROOT+'/slides',exist_ok=True)
INK='#1B1B2F';RED='#C62828';BG='#FFFDF9';FILM='#F3F1ED';SOFT='#FFF1F1';MUTE='#5E5E70';WHITE='#FFFFFF';GREEN='#1F7A4D'
F="font-family:Amiri, 'Times New Roman', serif"
VC='/_blob/6858107f89c3f1f8a734327a5afef175';LOGO='/_blob/854caf98e1d2f1e9e4cd1cfae3f5c7b3';U1='/_blob/fd90ff6edbb1c6569eb323553abc7084';U4='/_blob/eff4518818ab338dcd3b02fc16f37438';CARD='/_blob/9dbdabb27c742f641b9d306c5473cbf6'
RLM='\u200f'
def r(t):
    t=re.sub(r'([:·–…،؛؟!.«»\[\]()\-])', RLM+r'\1'+RLM, t); return RLM+t+RLM
def P(t,size=36,color=INK,extra=''):
    t=clean(t); check(t,'P')
    return f'<p style="font-size:{size}px;line-height:1.5;color:{color};text-align:right;{extra}">{r(t)}</p>'
def H(t,size=72,color=INK,tag='h2',extra=''):
    t=clean(t); check(t,'H')
    return f'<{tag} style="font-size:{size}px;font-weight:700;line-height:1.2;color:{color};text-align:right;{extra}">{r(t)}</{tag}>'
def K(t,color=RED): return P(t,34,color,'font-weight:700')
def foot(n,bg):
    c='#B8B8C8' if bg==INK else MUTE
    return f'<p style="position:absolute;right:128px;bottom:56px;width:900px;font-size:24px;color:{c};text-align:right">{r("مسار الفيديو")}</p><p style="position:absolute;left:128px;bottom:56px;width:200px;font-size:24px;color:{c};text-align:left">{n}</p>'
def card(title,text='',num=None,bg=WHITE,accent=RED):
    title=clean(title); text=clean(text); check(title,'card'); check(text,'card')
    n=f'<p style="font-size:30px;font-weight:700;color:{accent};text-align:right">{r(num)}</p>' if num else ''
    t=f'<p style="font-size:29px;line-height:1.5;color:{MUTE};text-align:right">{r(text)}</p>' if text else ''
    return f'<div style="flex:1;display:flex;flex-direction:column;gap:10px;background:{bg};padding:32px;border:2px solid {INK};border-radius:22px">{n}<h3 style="font-size:38px;font-weight:700;color:{INK};text-align:right">{r(title)}</h3>{t}</div>'
def row(*cells,gap=24): return f'<div style="display:flex;flex-direction:row-reverse;gap:{gap}px">{"".join(cells)}</div>'
def grid(cells,cols,gap=20):
    rows=[cells[i:i+cols] for i in range(0,len(cells),cols)]
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px">'+''.join(f'<div style="display:flex;flex-direction:row-reverse;gap:{gap}px">{"".join(x)}</div>' for x in rows)+'</div>'
def box(title,items,bg=WHITE,tc=RED,size=32):
    return f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{bg};border-radius:26px;padding:40px">'+H(title,40,tc,'h3')+''.join(P(x,size,INK) for x in items)+'</div>'
S=[];n=0
def add(id,body,notes,bg=BG,color=INK,layout='display:flex;flex-direction:column;gap:36px',pad='128px 128px 160px'):
    global n; n+=1
    b=body+(foot(n,bg) if id!='cover' else '')
    S.append((id,f'<section id="{id}" data-transition="fade" style="background:{bg};color:{color};{F};padding:{pad};{layout}">{b}<aside>{notes}</aside></section>'))

add('cover',
 f'<img src="{VC}" alt="غلاف حقيبة مسار الفيديو" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">'
 f'<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:{BG};opacity:0.9"></div>'
 f'<div style="position:absolute;right:128px;top:280px;width:1400px;display:flex;flex-direction:column;gap:22px">'
 +K('محاضرة تعريفية')+H('مسار الفيديو',120,INK,'h1')+H('أنتج الفيديو الخاص بك بالذكاء الاصطناعي',60,RED)
 +P('[اسمك]',34,MUTE)+P('[التاريخ]',30,MUTE)+'</div>',
 'دقيقة 0 إلى 1. رحّب بالحضور. قل: «قبل أن أعرّفكم بنفسي أو بالحقيبة، أريدكم أن تشاهدوا 49 ثانية.» ثم انتقل مباشرة إلى الإعلان.',
 layout='display:flex;flex-direction:column',pad='128px')

add('watch', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:32px">'
 f'<div style="width:1100px;height:619px;background:#000000;border-radius:28px;display:flex;align-items:center;justify-content:center"><p style="font-size:44px;color:#FFFFFF;text-align:center">{r("شغّل إعلان الحقيبة هنا")}</p></div>'
 +f'<p style="font-size:36px;color:#D8D8E4;text-align:center">{r("تسع وأربعون ثانية")}</p></div>',
 'دقيقة 1 إلى 2. شغّل الإعلان من ملف على حاسوبك (masar-video-promo.mp4)، لا من يوتيوب. في زوم: مشاركة الشاشة ثم فعّل «مشاركة الصوت» و«تحسين للفيديو». بعد انتهائه لا تتكلم ثانيتين، ثم انتقل.',
 bg=INK,color=WHITE,layout='display:flex;flex-direction:column')

add('reveal', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px">'
 +H('هذا الفيديو لم يُصوَّر',110,WHITE)+P('لا كاميرا ولا استوديو ولا ممثل',48,'#F2B8B8')
 +P('صُنع بالطريقة نفسها التي ستتعلمونها اليوم',44,WHITE)+'</div>',
 'دقيقة 2 إلى 4. قلها ببطء: «هذا الفيديو لم يُصوَّر. لا كاميرا، ولا استوديو. كتبنا نصه، وصنعنا صوته، وأنتجناه بالذكاء الاصطناعي، خطوة بخطوة. وفي الساعة القادمة سأريكم الطريق نفسه.» هذه أقوى لحظة في المحاضرة: لا تستعجل بعدها.',
 bg=RED,color=WHITE)

add('poll', H('سؤال سريع',72)+
 f'<div style="display:flex;flex-direction:column;gap:26px;background:{WHITE};border:2px solid {RED};border-radius:28px;padding:52px">'
 +H('هل حاولت صنع فيديو بالذكاء الاصطناعي',54,INK,'h3')
 +row(card('نعم وتوقفت','','أ'),card('نعم ونجحت','','ب'),card('لم أحاول بعد','','ج'))+'</div>'
 +P('أجب في الاستطلاع أو اكتب الحرف في الدردشة',32,MUTE),
 'دقيقة 4 إلى 6. شغّل استطلاع زوم. الأغلب يختار «نعم وتوقفت» أو «لم أحاول». علّق: «من توقف، غالبًا توقف لأنه بدأ بالأداة. سأريكم لماذا.»')

add('problem', K('المشكلة')+H('تبدأ بالأداة',96)+
 P('فتصنع ما تحسنه الأداة، لا ما يحتاجه جمهورك',52,RED,'font-weight:700')
 +P('ثم تدفع مرة بعد مرة لتصحح ما كان يمكن تصحيحه مجانًا',40,MUTE),
 'دقيقة 6 إلى 8. مثال: «من يفتح أداة أفاتار أولًا، يصنع أفاتار لكل شيء، حتى لو كان شرح برنامج يكفيه تسجيل الشاشة.» واذكر أن كل إعادة توليد في الأدوات المدفوعة تُدفع من جديد.')

add('principles', H('ثلاث أفكار تحمل الحقيبة كلها',68)+
 row(card('القرار قبل الأداة','بطاقة من سبعة أسئلة قبل أي ضغطة','1'),card('الصوت هو العمود الفقري','يُصنع أولًا والمشاهد تُقص عليه','2'),card('المجاني أولًا','والمدفوع مرة واحدة بعد التصحيح','3')),
 'دقيقة 8 إلى 11. هذه الشريحة الملخص. قل: «إن تذكرتم ثلاث جمل من اليوم، فهي هذه.» اشرح الثالثة بمثال: «نراجع الفيديو كاملًا بصورة ثابتة مجانًا، ثم نولّد المقدّم المدفوع مرة واحدة.»')

units=[('البطاقة','سبعة أسئلة'),('النص','اكتب للأذن'),('الصوت','نصف الفيديو'),('الصورة','عشرة أشكال'),('المونتاج','الصوت أولًا'),('النشر','افحص وانشر')]
add('path', H('الطريق في ست وحدات',72)+grid([card(a,b,str(i+1)) for i,(a,b) in enumerate(units)],3)
 +P('مخرج كل وحدة هو مدخل الوحدة التي بعدها',38,RED,'font-weight:700'),
 'دقيقة 11 إلى 13. اقرأ الوحدات من اليمين: البطاقة ثم النص ثم الصوت، ثم الصورة ثم المونتاج ثم النشر. قل: «في نهاية الحقيبة، معك فيديو حقيقي منشور عن موضوعك.»')

add('try', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:30px">'
 +H('لنطبّق الآن معًا',100,WHITE)+P('اكتب في الدردشة فيديو تحتاجه لعملك',50,'#F3F1ED')
 +P('مثال',30,'#F2B8B8','font-weight:700')+P('فيديو يشرح خدمة مشروعي في دقيقة',36,'#B8B8C8')+'</div>',
 'دقيقة 13 إلى 15. انتظر 30 إلى 60 ثانية. اقرأ ثلاثة أمثلة، واختر واحدًا تطبّق عليه البطاقة في الشريحة التالية. اشكر صاحبه بالاسم.',
 bg=INK,color=WHITE)

seven=['الغرض','الجمهور','الرسالة الواحدة','الشكل','الصوت','الإضافات','القيود']
add('u1', K('الوحدة الأولى')+H('سبعة أسئلة قبل أي أداة',64)+grid([card(x,num=str(i+1)) for i,x in enumerate(seven[:4])],4)
 +grid([card(x,num=str(i+5)) for i,x in enumerate(seven[4:])],3)
 +P('الدقيقة الواحدة نحو مئة وعشر كلمات',36,RED,'font-weight:700'),
 'دقيقة 15 إلى 21. طبّق الأسئلة السبعة على مثال الحاضر سريعًا: ما الغرض؟ من الجمهور؟ ما الرسالة الواحدة؟ ثم احسب الكلمات: فيديو دقيقة يعني نحو 110 كلمات. قل: «هذا الحساب البسيط يمنعك من نص أطول من اللازم، وتكلفة أعلى من اللازم.» سؤال متوقع: «هل أحتاج كل الأسئلة؟» الجواب: نعم، لأن الأسئلة الثلاثة الأخيرة هي وحدات لاحقة.')

add('u2', K('الوحدة الثانية')+H('اكتب للأذن لا للعين',64)+
 row(box('قبل',['«نقدّم لكم دورة متميزة في صناعة المحتوى باستخدام أحدث التقنيات لتطوير مهاراتكم»'],SOFT,RED,36),
     box('بعد',['«تريد فيديو لمشروعك؟ في ست خطوات تصنعه بنفسك»'],'#E9F4EE',GREEN,40))
 +P('جملة قصيرة وفكرة واحدة والمهم أولًا',38,INK,'font-weight:700'),
 'دقيقة 21 إلى 25. اقرأ الجملتين بصوت مسموع، واسأل: «أيهما تفهمونها من سماعها مرة واحدة؟» ثم القواعد الأربع: 12 كلمة أو أقل، فكرة واحدة، المهم أولًا، والأرقام كلمات كما تُنطق.')

add('u3', K('الوحدة الثالثة')+H('الصوت نصف الفيديو',64)+
 grid([card('صوتك','مجاني'),card('صوت مولّد','سنتات'),card('دبلجة','الأغلى'),card('بلا تعليق','مجاني')],4)
 +P('المشاهد يسامح صورة متوسطة ولا يسامح صوتًا سيئًا',40,RED,'font-weight:700'),
 'دقيقة 25 إلى 30. القاعدة: إن كان وجهك أو اسمك في الفيديو فصوتك أولى، وإن كانت سلسلة ستُعدَّل كثيرًا فالمولّد أنسب. نصيحة يحبها الحضور: «الغرفة الهادئة والهاتف على بعد شبر أهم من الميكروفون الغالي.»')

FITS={'شرائح مع صوت': 'الدرس والتقرير', 'أفاتار': 'الدرس المتكرر والإعلان القصير', 'أمام الكاميرا': 'المقابلة والتعريف بنفسك', 'تسجيل الشاشة': 'شرح برنامج أو موقع', 'رسم باليد': 'فكرة تتكوّن تدريجيًا', 'رسوم متحركة': 'الإعلان والأطفال', 'مشاهد مولّدة': 'الإعلان والقصة', 'صور متحركة': 'القصة والتهنئة', 'مونتاج لقطات': 'ملخص الفعالية', 'ترجمة أو دبلجة': 'فيديو موجود بلغة أخرى'}
def scard(name,i):
    return f'<div style="flex:1;display:flex;flex-direction:column;gap:10px;align-items:flex-end;background:{WHITE};padding:22px;border:2px solid {INK};border-radius:22px">{SHAPESVG[name]}<p style="font-size:26px;font-weight:700;color:{RED};text-align:right">{r(str(i))}</p><h3 style="font-size:32px;font-weight:700;color:{INK};text-align:right">{r(name)}</h3><p style="font-size:24px;color:{MUTE};text-align:right">{r(clean(FITS[name]))}</p></div>'
names=list(FITS)
add('u4', K('الوحدة الرابعة')+H('عشرة أشكال للصورة',64)+row(*[scard(x,i+1) for i,x in enumerate(names[:5])],gap=18),
 'دقيقة 30 إلى 32. الأشكال الخمسة الأولى. اشرح كل شكل في جملة واحدة مع الرسم: الشرائح عرض تقديمي يُقرأ عليه صوت، والأفاتار شخصية رقمية تتحرك شفتاها على الصوت، وأمام الكاميرا تصوّر نفسك بهاتفك، وتسجيل الشاشة لشرح برنامج، والرسم باليد هاتف فوق ورقة تتكون عليها الفكرة.')
add('u4b', K('الوحدة الرابعة')+H('عشرة أشكال للصورة',64)+row(*[scard(x,i+6) for i,x in enumerate(names[5:])],gap=18),
 'دقيقة 32 إلى 34. الأشكال الخمسة الباقية: الرسوم المتحركة شخصيات مرسومة تتحرك، والمشاهد المولّدة لقطات تصنعها أداة من وصف مكتوب، والصور المتحركة صور ثابتة تتحرك ببطء، ومونتاج اللقطات تجميع مقاطع صورتها، والترجمة أو الدبلجة لفيديو موجود. ثم قل: أغلب الدورات تعلّم الأفاتار وحده، وهو الأغلى، والدرس يكفيه شرائح.')
add('real', K('من فيديوهات الحقيبة نفسها')+H('شكلان في فيديو واحد',64)+
 row(f'<div style="flex:1;display:flex;flex-direction:column;gap:14px"><img src="/_blob/8441bdec80c9fd30ea54fd6d23ed0834" alt="المقدّم الرقمي في إعلان الحقيبة" style="width:780px;height:439px;object-fit:cover;border-radius:20px">'+P('أفاتار في البداية والنهاية',34,INK,'font-weight:700')+'</div>',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:14px"><img src="/_blob/fd2a688e6311a64b00db988c3858319a" alt="شرائح الوحدات في إعلان الحقيبة" style="width:780px;height:439px;object-fit:cover;border-radius:20px">'+P('وشرائح مع صوت في الوسط',34,INK,'font-weight:700')+'</div>'),
 'دقيقة 34 إلى 35. مثال حقيقي يفهمه الجميع: إعلان الحقيبة الذي شاهدوه في البداية يخلط شكلين: المقدّم الرقمي (أفاتار) في الافتتاح والختام لأنه يجذب، والشرائح في الوسط لأنها تشرح وتُقرأ، والأفاتار يُدفع بالثانية فنستعمله حيث يخدم فقط.')

rows=[('درس','شرائح مع صوت'),('شرح برنامج','تسجيل الشاشة'),('إعلان','مشاهد مولّدة أو أفاتار قصير'),('مقابلة','أمام الكاميرا'),('ملخص فعالية','مونتاج لقطات')]
trs=''.join(f'<tr><td style="text-align:right">{r(b)}</td><td style="text-align:right">{r(a)}</td></tr>' for a,b in rows)
add('purpose', K('القاعدة')+H('الغرض يختار الشكل',64)+
 f'<table style="font-size:34px;color:{INK}"><tr><th style="width:60%;text-align:right">{r("الشكل الأنسب غالبًا")}</th><th style="width:40%;text-align:right">{r("الغرض")}</th></tr>{trs}</table>',
 'دقيقة 34 إلى 37. ارجع إلى مثال الحاضر: ما غرضه؟ إذن ما الشكل الأنسب؟ إن كان إعلانًا قصيرًا، اذكر أن المدفوع يُحسب بالثانية، فنحسب التكلفة قبل الضغط.')

add('u5', K('الوحدة الخامسة')+H('المونتاج والإضافات',64)+
 row(card('الصوت أولًا','على المسار السفلي','1'),card('المشاهد فوقه','كل مشهد مع أول كلمة','2'),card('قطع مباشر','والتلاشي بين الأقسام فقط','3'),card('شاهد كاملًا','قبل أي إضافة','4'))
 +P('أضف ما كتبته في بطاقتك فقط',38,RED,'font-weight:700'),
 'دقيقة 37 إلى 41. أداة المتدرب المقترحة CapCut (الهاتف والحاسوب)، والبديل DaVinci Resolve. نبّه على الموسيقى: «وجدتها على الإنترنت ليست ترخيصًا»، واستعمل مكتبة يوتيوب الصوتية أو Pixabay Music.')

add('u6', K('الوحدة السادسة')+H('افحص على الهاتف ثم انشر',64)+
 row(box('خمسة فحوص',['بسماعة','بلا صوت','الأطراف','الأسماء والأرقام','مشاهد من الجمهور'],WHITE,RED,30),
     box('ثم',['انشر غير مدرج أولًا','أفصح عن المحتوى المولّد','اكتب بطاقة القرار'],SOFT,RED,32)),
 'دقيقة 41 إلى 45. الفحص الخامس أذكاها: «يشاهد شخص من الجمهور ثم يقول الرسالة الواحدة بكلماته. إن لم يقلها، فالفيديو لم يوصلها.» وبطاقة القرار تجعل الفيديو الثاني أفضل بسبب واضح.')

stages=[('السيناريو','يُكتب ويُعتمد'),('الصوت','جملة جملة'),('المسودة الصامتة','تُراجع مجانًا'),('المقدّم','يُولّد مرة واحدة'),('التركيب','والنشر')]
add('proof', K('الدليل')+H('كيف صنعنا فيديوهات الحقيبة',64)+grid([card(a,b,str(i+1)) for i,(a,b) in enumerate(stages)],5,16)
 +row(f'<img src="{U1}" alt="الصورة المصغرة للوحدة الأولى" style="width:520px;height:292px;object-fit:cover;border-radius:18px">',f'<img src="{U4}" alt="الصورة المصغرة للوحدة الرابعة" style="width:520px;height:292px;object-fit:cover;border-radius:18px">'),
 'دقيقة 45 إلى 49. هنا للزوار والزملاء معًا. لا تذكر أرقام التكلفة. قل: «كل فيديو من الستة مرّ بهذه الخطوات الخمس. والمسودة الصامتة هي سر التوفير: نراجع الفيديو كاملًا قبل أي دفع.» إن سألك زميل عن الأدوات: الصوت مولّد بنموذج متعدد اللغات، والمقدّم أداة تحريك صورة بالصوت.')

add('lesson', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px">'
 +K('أغلى درس تعلّمناه','#F2B8B8')+H('جرّب صغيرًا أولًا',104,WHITE)
 +P('جرّبنا طريقة جديدة كاملة دون مقطع تجريبي فدفعنا ثمن الخطأ',42,'#F3F1ED')
 +P('وأنتم تتعلمون القاعدة دون أن تدفعوا ثمنها',44,WHITE,'font-weight:700')+'</div>',
 'دقيقة 49 إلى 51. احكِ قصة الحوار بين شخصين في الوحدة الرابعة، دون أرقام مالية: «أردنا حوارًا، فجرّبنا طرقًا كاملة لم نختبرها بمقطع صغير، ففشلت. ومنذ ذلك اليوم: أي طريقة جديدة تبدأ بتجربة صغيرة.» هذه القصة تبيع الحقيبة: صدق وخبرة حقيقية.',
 bg=INK,color=WHITE)

add('inside', H('ماذا تجد داخل الحقيبة',68)+
 row(f'<img src="{CARD}" alt="ورقة عمل بطاقة الفيديو" style="width:760px;height:540px;object-fit:contain;background:{FILM};border-radius:20px">',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:16px;justify-content:center">'+''.join(P(x,34,INK) for x in ['ست فيديوهات قصيرة بمقدّم','ستة ملفات بأوراق عمل قابلة للكتابة','برومبت جاهز وبديل مجاني لكل مرحلة','امتحان قصير لكل وحدة','شهادة إتمام'])+'</div>'),
 'دقيقة 51 إلى 55. شغّل فيديو الجولة المسجل (3 دقائق) أو ادخل منصة CPS كمتدرب: وحدة واحدة كاملة: الفيديو، ثم الملف، ثم الامتحان. أشر إلى أن أوراق العمل تُكتب على الحاسوب مباشرة.')

add('offer', K('لحضور هذه المحاضرة')+H('عرض الإطلاق',80)+
 row(f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{WHITE};border:2px solid {INK};border-radius:26px;padding:44px">'+P('السعر',32,MUTE)+H('خمسة وعشرون دولارًا',58,INK,'h3')+'</div>',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{SOFT};border:2px solid {RED};border-radius:26px;padding:44px">'+P('خصم الإطلاق',32,RED,'font-weight:700')+H('أربعون بالمئة',58,RED,'h3')+P('لأول عشرين مشتركًا',32,INK)+P('حتى [تاريخ انتهاء العرض]',30,MUTE)+'</div>')
 +P('ولمن يريد البداية مجانًا',30,MUTE)+P('الحقيبة المجانية مسار الذكاء الاصطناعي',34,INK,'font-weight:700'),
 'دقيقة 55 إلى 57. اذكر العرض مرة واحدة بوضوح، دون إلحاح. اكتب رمز الكوبون في الدردشة. لمن لا يريد الدفع الآن: «ابدؤوا بالحقيبة المجانية، فهي باب المنهج نفسه.» تأكد قبل المحاضرة أن الحقيبة مفعّلة وأن الكوبون يعمل.')

add('cta', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:26px">'
 +H('سجّل الآن',110,WHITE)+P('[رابط التسجيل في الحقيبة على منصة CPS]',44,'#F2B8B8','font-weight:700')
 +P('[رمز الكوبون]',40,WHITE)+P('الرابط في الدردشة الآن',34,'#F3F1ED')+P('[ضع رمز QR هنا]',30,'#B8B8C8')+'</div>',
 'دقيقة 57 إلى 58. الصق الرابط ورمز الكوبون في الدردشة. اترك الشريحة ظاهرة 20 ثانية.',
 bg=RED,color=WHITE)

add('qa', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:26px">'
 f'<img src="{LOGO}" alt="شعار مسار" style="width:400px;height:202px;object-fit:contain">'
 +f'<h2 style="font-size:110px;font-weight:700;color:{INK};text-align:center">{r("أسئلتكم")}</h2>'
 +f'<p style="font-size:38px;color:{MUTE};text-align:center">{r("اكتبها في الدردشة أو ارفع يدك")}</p></div>',
 'دقيقة 58 إلى 75. أسئلة الزوار المتوقعة: هل أحتاج خبرة أو حاسوبًا؟ (لا، الهاتف يكفي). هل أحتاج أن أدفع لأدوات؟ (لا، لكل مرحلة بديل مجاني). كم المدة؟ (نحو 4 ساعات، والإيقاع المقترح أسبوعان). هل يقبل يوتيوب الفيديو المصنوع بالذكاء الاصطناعي؟ (نعم، مع الإفصاح عن المحتوى الواقعي المولّد). أسئلة الزملاء: كم كلّف الإنتاج؟ (قل: «تكلفة منخفضة بفضل المسودة الصامتة»، ولا تذكر رقمًا أمام المشترين). هل كتب الذكاء الاصطناعي الحقيبة؟ («الأدوات نفّذت، وأنا قررت المنهج والجمهور والأشكال، وراجعت كل فيديو»). كيف أصنع حقيبتي بالطريقة نفسها؟ (المنهجية الأربع والعشرون، وجرّب صغيرًا أولًا). اختم بالشكر وإعادة الرابط.',
 bg=BG)

order=[i for i,_ in S]
for i,h in S: open(f'{ROOT}/slides/{i}.html','w',encoding='utf-8').write(h)
deck={"v":4,"createdOnFiles":{"v":1,"at":datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},"lists":"css","title":"محاضرة: مسار الفيديو — من بطاقة إلى فيديو منشور","order":order,
 "sections":{"s1":{"description":"الإعلان والمشكلة","start":"cover"},"s2":{"description":"الطريق في ست وحدات وتطبيقه حيًا","start":"principles"},"s3":{"description":"الدليل وداخل الحقيبة","start":"proof"},"s4":{"description":"العرض والدعوة والأسئلة","start":"offer"}},
 "cover":"cover","faces":{"amiri":{"family":"Amiri","href":"https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"}},"designSystems":[]}
json.dump(deck,open(f'{ROOT}/deck.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(order)); print('WARN',WARN); print(json.dumps([f'{ROOT}/slides/{x}.html' for x in order[1:15]])); print(json.dumps([f'{ROOT}/slides/{x}.html' for x in order[15:]]))
