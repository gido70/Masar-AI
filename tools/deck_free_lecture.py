import json, os, datetime
ROOT='/mnt/user-data/outputs/artifacts/4d8c2ca8-0820-42d8-ac7d-9c204e321a13/project'
os.makedirs(ROOT+'/slides',exist_ok=True)
NAVY='#123E6B';CREAM='#FFFCF3';TEAL='#0E7C8C';GOLD='#C9971F';INK='#1F2A37';SOFT='#E8F4F3';MUTE='#5A6472';GSOFT='#FBF4E2';WHITE='#FFFEFA'
F="font-family:Amiri, 'Times New Roman', serif"
LOGO='/_blob/ab91417303310682270b17380d93d48f';COVER='/_blob/22ee2c7911fedbb3c1b6cc2a5469d523';WB='/_blob/140a5c2b4d5cb0e8561dfd7781880f48';U1='/_blob/c3b4cef2d69679e70002a50b01cf6780';VC='/_blob/d5adfb9bb219ad5f1e0a76a85f15636d'
RLM='\u200f'
def r(t):
    import re
    t=re.sub(r'([:·–…،؛؟!.«»\[\]()\-])', RLM+r'\1'+RLM, t)
    return RLM+t+RLM
def P(t,size=36,color=INK,w=None,extra=''): return f'<p style="font-size:{size}px;line-height:1.5;color:{color};text-align:right;{extra}">{r(t)}</p>'
def H(t,size=72,color=NAVY,tag='h2',extra=''): return f'<{tag} style="font-size:{size}px;font-weight:700;line-height:1.2;color:{color};text-align:right;{extra}">{r(t)}</{tag}>'
def foot(n,bg=CREAM): 
    c=MUTE if bg!=NAVY else '#C9D6E3'
    return f'<p style="position:absolute;right:128px;bottom:56px;width:900px;font-size:24px;color:{c};text-align:right">{r("مسار الذكاء الاصطناعي")}</p><p style="position:absolute;left:128px;bottom:56px;width:200px;font-size:24px;color:{c};text-align:left">{n}</p>'
def sec(id,body,notes,bg=CREAM,color=INK,layout='display:flex;flex-direction:column;gap:40px',pad='128px 128px 160px'):
    return f'<section id="{id}" data-transition="fade" style="background:{bg};color:{color};{F};padding:{pad};{layout}">{body}<aside>{notes}</aside></section>'
def card(title,text,num=None,bg=WHITE,accent=TEAL):
    n=f'<p style="font-size:30px;font-weight:700;color:{accent};text-align:right">{r(num)}</p>' if num else ''
    return f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{bg};padding:36px;border:1px solid #E6DFC8;border-radius:24px">{n}<h3 style="font-size:40px;font-weight:700;color:{NAVY};text-align:right">{r(title)}</h3><p style="font-size:30px;line-height:1.5;color:{MUTE};text-align:right">{r(text)}</p></div>'
def grid(cells,cols,gap=20):
    rows=[cells[i:i+cols] for i in range(0,len(cells),cols)]
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px">'+''.join(f'<div style="display:flex;flex-direction:row-reverse;gap:{gap}px">{"".join(r_)}</div>' for r_ in rows)+'</div>'
def row(*cells,gap=28): return f'<div style="display:flex;flex-direction:row-reverse;gap:{gap}px">{"".join(cells)}</div>'
S=[]
n=0
def add(id,body,notes,**k):
    global n; n+=1
    b=body+(foot(n,k.get('bg',CREAM)) if id!='cover' else '')
    S.append((id,sec(id,b,notes,**k)))

add('cover',
 f'<img src="{COVER}" alt="غلاف الحقيبة" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">'
 f'<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:#FFFCF3;opacity:0.82"></div>'
 f'<div style="position:absolute;right:128px;top:300px;width:1300px;display:flex;flex-direction:column;gap:24px">'
 +P('محاضرة تعريفية لحقيبة مجانية',34,TEAL,extra='font-weight:700')
 +H('مسار الذكاء الاصطناعي',110,NAVY,'h1')
 +H('من التشتت إلى قرار وتنفيذ ذكي',64,TEAL)
 +P('[اسمك]',34,MUTE)+P('[التاريخ]',30,MUTE)+'</div>',
 'دقيقة 0 إلى 1. رحّب بالحضور بالاسم إن أمكن. قل: «في الساعة القادمة سنتعلم معًا طريقة تختصر عليكم ساعات من التجريب مع أدوات الذكاء الاصطناعي، وسنطبّقها على مهام حقيقية منكم في الدردشة.» قبل البدء: تأكد أن الصوت يعمل، وأن الشاشة مشاركة بوضع العرض الكامل.',
 bg=CREAM,layout='display:flex;flex-direction:column',pad='128px')

add('poll', H('سؤال سريع قبل أن نبدأ',72)+
 f'<div style="display:flex;flex-direction:column;gap:28px;background:{WHITE};border:2px solid {TEAL};border-radius:28px;padding:56px">'
 +H('كم أداة ذكاء اصطناعي جرّبت هذا الشهر؟',56,INK,'h3')
 +row(card('أداة واحدة','','أ'),card('من 2 إلى 5','','ب'),card('أكثر من 5','','ج'))+'</div>'
 +P('أجب في الاستطلاع، أو اكتب الحرف في الدردشة',32,MUTE),
 'دقيقة 1 إلى 4. شغّل استطلاع زوم (Polls) بالخيارات الثلاثة، أو اطلب كتابة الحرف في الدردشة. اقرأ النتيجة بصوت مسموع. الأغلب سيختار «من 2 إلى 5» أو «أكثر من 5». علّق: «إذن نحن متفقون: المشكلة ليست قلة الأدوات.» وانتقل.')

add('problem',
 f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px">'
 +H('يفتح أدوات كثيرة',96,'#FFFFFF','h2')+H('ويجرّب الأكثر شهرة',96,'#FFFFFF','h2')+H('ويضيع وقته',96,'#F2C94C','h2')+'</div>',
 'دقيقة 4 إلى 7. هذه الشريحة قصة يعرفها كل الحضور. احكها بصيغة شخصية: «أردت مرة أن أصنع عرضًا تقديميًا، ففتحت خمس أدوات، وبعد ساعتين لم يكن عندي شيء.» اسأل: «من مرّ بهذا؟ اكتب نعم في الدردشة.» انتظر ثواني، ثم انتقل.',
 bg=NAVY,color='#FFFFFF')

add('cause', H('أين المشكلة الحقيقية؟',72)+
 row(f'<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:#FBEDE8;border-radius:28px;padding:48px"><p style="font-size:30px;color:#A8492F;font-weight:700;text-align:right">{r("ما نظنه")}</p><h3 style="font-size:52px;color:{INK};text-align:right">{r("نحتاج أداة أفضل")}</h3></div>',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:{SOFT};border-radius:28px;padding:48px"><p style="font-size:30px;color:{TEAL};font-weight:700;text-align:right">{r("الحقيقة")}</p><h3 style="font-size:52px;color:{INK};text-align:right">{r("المهمة لم تكن واضحة من البداية")}</h3></div>')
 +P('قبل أن تسأل «ما الأداة؟»، اسأل: «ماذا أريد بالضبط؟»',44,NAVY,extra='font-weight:700'),
 'دقيقة 7 إلى 10. الفكرة المركزية للحقيبة كلها. قلها ببطء: «المهمة الغامضة تجعل كل الأدوات تبدو مناسبة. حين تتحدد المهمة، يسقط أغلب الأدوات وحده.» هذه الجملة الأخيرة على الشريحة كررها مرتين.')

add('package', H('ما هي الحقيبة؟',72)+
 row(card('خمس وحدات','فيديو قصير وملف لكل وحدة','1'),card('كراسة أدوات العمل','خمس أوراق تكتب فيها على مهمتك الحقيقية','2'),card('امتحان وشهادة','امتحان قصير لكل وحدة، وشهادة إتمام','3'))
 +P('مجانية، على منصة CPS، وتطبّقها على مهمة من عملك أنت',40,TEAL,extra='font-weight:700'),
 'دقيقة 10 إلى 12. لا تطل هنا: الشريحة تمهيد. أكد أن الحقيبة مجانية، وأن كل ورقة عمل تُملأ على مهمة حقيقية من عمل المتدرب لا على مثال جاهز. قل: «سأريكم الآن الطريق كاملًا، ثم نطبّقه معًا.»')

steps=[('1','المهمة','العناصر الأربعة'),('2','الجمهور والقيود','لمن؟ وبأي حدود؟'),('3','مقارنة أداتين','خمسة معايير'),('4','القرار والبرومبت','ستة عناصر'),('5','التنفيذ والتحقق','نسخة صغيرة أولًا')]
cells=''.join(f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{WHITE};border:3px solid {NAVY};border-radius:24px;padding:28px"><p style="font-size:34px;font-weight:700;color:{GOLD};text-align:right">{r(a)}</p><h3 style="font-size:38px;color:{NAVY};text-align:right">{r(b)}</h3><p style="font-size:28px;color:{MUTE};text-align:right">{r(c)}</p></div>' for a,b,c in steps)
add('path', H('الطريق في خمس خطوات',72)+f'<div style="display:flex;flex-direction:row-reverse;gap:20px">{cells}</div>'
 +P('مخرج كل خطوة هو مدخل الخطوة التي بعدها: لا يمكن القفز',38,NAVY,extra='font-weight:700'),
 'دقيقة 12 إلى 15. اقرأ الخطوات الخمس من اليمين إلى اليسار. ثم قل الجملة السفلى: «لا تستطيع أن تقارن أدوات قبل أن تعرف جمهورك وقيودك، ولا تكتب برومبت قبل أن تختار الأداة.» هذه خريطة المحاضرة أيضًا.')

add('try', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:32px">'
 +H('لنطبّق الآن معًا',96,'#FFFFFF','h2')
 +P('اكتب في الدردشة: مهمة واحدة تريد إنجازها بالذكاء الاصطناعي',48,'#E8F4F3')
 +P('مثال: «أريد عرضًا تقديميًا لمحاضرتي» أو «أريد تلخيص تقرير طويل»',36,'#C9D6E3')+'</div>',
 'دقيقة 15 إلى 17. هذا قلب التفاعل. اطلب من الحضور كتابة مهمة في الدردشة، وانتظر 30 إلى 60 ثانية. اقرأ ثلاث مهام بصوت مسموع، واختر واحدة عامة (مثل «أريد عرضًا تقديميًا») لتطبّق عليها الخطوات في الشرائح القادمة. اكتب اسم صاحبها وشكره. إن كان الحضور قليلًا، استخدم المثال الجاهز على الشريحة.',
 bg=TEAL,color='#FFFFFF')

four=[('الفعل المطلوب','ماذا تريد أن تنفذ؟','كتابة، تلخيص، تحليل'),('الموضوع','ما الذي ستعمل عليه؟','محاضرة، تقرير، فكرة'),('المخرج النهائي','بأي شكل تستلمه؟','عرض، جدول، فيديو'),('معيار النجاح','ما صفاته؟','بالعربية، مختصر، 5 دقائق')]
add('u1', P('الوحدة 1',34,TEAL,extra='font-weight:700')+H('العناصر الأربعة للمهمة الواضحة',64)+
 grid([card(a,b+' مثل '+c) for a,b,c in four],2,24)
 +P('«أريد أن أنفذ [الفعل] حول [الموضوع] في صورة [المخرج] لجمهور [الجمهور] مع الالتزام بـ[القيود]»',32,NAVY,extra=f'background:{GSOFT};border-radius:20px;padding:24px 32px'),
 'دقيقة 17 إلى 22. اشرح العناصر الأربعة، ثم طبّقها مباشرة على مهمة الحاضر التي اخترتها: ما الفعل؟ ما الموضوع؟ ما المخرج؟ ما معيار النجاح؟ اكتب الإجابات في الدردشة بنفسك أو قلها. ثم اقرأ قالب الصياغة في الأسفل. سؤال متوقع: «الفيديو فعل؟» الجواب: لا، الفيديو مخرج، والفعل أشرح أو أعلن أو أوثّق.')

add('example', H('قبل وبعد',72)+
 row(f'<div style="flex:1;display:flex;flex-direction:column;gap:20px;background:#FBEDE8;border-radius:28px;padding:48px"><p style="font-size:30px;font-weight:700;color:#A8492F;text-align:right">{r("طلب عام: يشتت")}</p><h3 style="font-size:46px;line-height:1.4;color:{INK};text-align:right">{r("«أريد استخدام الذكاء الاصطناعي لعمل فيديو»")}</h3></div>',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:20px;background:{SOFT};border-radius:28px;padding:48px"><p style="font-size:30px;font-weight:700;color:{TEAL};text-align:right">{r("طلب محدد: يوفر الوقت")}</p><h3 style="font-size:40px;line-height:1.45;color:{INK};text-align:right">{r("«أريد فيديو تعليميًا عربيًا من 3 إلى 5 دقائق، يشرح فكرة واحدة للمبتدئين، بشرائح واضحة وتعليق هادئ»")}</h3></div>')
 +P('الثاني يحدد الأدوات المناسبة قبل أن تبحث عنها',40,NAVY,extra='font-weight:700'),
 'دقيقة 22 إلى 25. اقرأ الطلبين. اسأل الحضور: «أيهما يعطيك نتيجة أسرع؟» ثم أعد صياغة مهمة الحاضر بالطريقة نفسها، واقرأها كاملة. هذه لحظة «آها»: يرون مهمتهم تتحول من غامضة إلى واضحة.')

add('u2', P('الوحدة 2',34,TEAL,extra='font-weight:700')+H('الجمهور والقيود',64)+
 row(f'<div style="flex:1;display:flex;flex-direction:column;gap:14px;background:{WHITE};border:1px solid #E6DFC8;border-radius:24px;padding:40px"><h3 style="font-size:40px;color:{NAVY};text-align:right">{r("أربعة أسئلة عن الجمهور")}</h3>'+''.join(P(x,32,INK) for x in ['من سيستخدم الناتج؟','ماذا يعرف مسبقًا؟','أين سيشاهده؟','ما اللغة والأسلوب المناسبان؟'])+'</div>',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:14px;background:{GSOFT};border-radius:24px;padding:40px"><h3 style="font-size:40px;color:{NAVY};text-align:right">{r("القيود معايير، لا عوائق")}</h3>'+''.join(P(x,32,INK) for x in ['الوقت والميزانية','الخصوصية والبيانات','الجهاز والاتصال','طول المحتوى وصيغته'])+'</div>')
 +P('كل قيد يحذف أدوات لا تناسبك، فتختصر المقارنة قبل أن تبدأ',38,TEAL,extra='font-weight:700'),
 'دقيقة 25 إلى 29. طبّق على مهمة الحاضر: من الجمهور؟ هاتف أم حاسوب؟ مجاني أم مدفوع؟ ثم قل الجملة المهمة: «مجاني تمامًا يحذف الأدوات المدفوعة، وهاتف فقط يحذف برامج الحاسوب.» القيود تختصر الطريق.')

crit=['جودة النتيجة','سهولة الاستخدام','دعم اللغة العربية','الكلفة','الخصوصية']
rows=''.join(f'<tr><td style="text-align:center"> </td><td style="text-align:center"> </td><td style="text-align:right">{r(c)}</td></tr>' for c in crit)
add('u3', P('الوحدة 3',34,TEAL,extra='font-weight:700')+H('أداتان فقط وخمسة معايير',64)+
 row(f'<table style="flex:1.3;font-size:32px;color:{INK}"><tr><th style="width:25%;text-align:center">{r("الأداة ب")}</th><th style="width:25%;text-align:center">{r("الأداة أ")}</th><th style="width:50%;text-align:right">{r("المعيار")}</th></tr>{rows}</table>',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:20px;justify-content:center">'+P('درجة من 1 إلى 5 لكل معيار',36,INK)+P('نقطة قوة ونقطة ضعف لكل أداة',36,INK)+P('اختر الأعلى توافقًا مع قيودك، لا الأشهر',40,TEAL,extra='font-weight:700')+'</div>'),
 'دقيقة 29 إلى 34. اشرح لماذا أداتان لا عشر: «المقارنة بين عشر أدوات تعيد التشتت الذي جئنا لعلاجه. واثنتان تكفيان لقرار مبرَّر، والثانية بديل جاهز إن فشلت الأولى.» إن أمكن، قارن أداتين لمهمة الحاضر شفهيًا على معيارين فقط. سؤال متوقع: «كيف أعرف الأداتين؟» الجواب: من القيود، أو اسأل مساعدًا ذكيًا بعد أن تعطيه بطاقتك.')

six=[('الدور','مدرب، كاتب، محلل'),('المهمة','اكتب، لخّص، قارن'),('السياق','الموضوع والجمهور والغرض'),('القيود','اللغة والمدة والأسلوب'),('صيغة المخرج','نص، جدول، عرض'),('معيار الجودة','دقيق، واضح، موثوق')]
add('u4', P('الوحدة 4',34,TEAL,extra='font-weight:700')+H('ستة عناصر للبرومبت',64)+
 grid([card(a,b,str(i+1)) for i,(a,b) in enumerate(six)],3)
 +P('البرومبت لا يُكتب من فراغ: هو بطاقة مهمتك مكتوبة بلغة الأداة',38,NAVY,extra='font-weight:700'),
 'دقيقة 34 إلى 40. لاحظ مع الحضور: أربعة من العناصر الستة (المهمة والسياق والقيود والمخرج) جاءت من الوحدتين 1 و2. ثم اكتب برومبت مهمة الحاضر كاملًا في الدردشة بالعناصر الستة. هذه أقوى لحظة تطبيقية: يرون كيف تحولت جملة غامضة إلى تعليمات كاملة في 20 دقيقة.')

add('u5', P('الوحدة 5',34,TEAL,extra='font-weight:700')+H('لا تعتمد أول نتيجة',64)+
 row(card('نفّذ نسخة صغيرة','جزء من المهمة أولًا','1',accent=GOLD),card('افحصها','الدقة، والاكتمال، وملاءمة الجمهور، والقيود','2',accent=GOLD),card('عدّل التعليمات','العلاج غالبًا في التعليمات لا في الأداة','3',accent=GOLD),card('اعتمد','بعد أن تجيب «نعم» عن قائمة التحقق','4',accent=GOLD))
 +P('أي «لا» في قائمة التحقق تعني: لا تعتمد بعد',38,TEAL,extra='font-weight:700'),
 'دقيقة 40 إلى 44. القاعدة الأخيرة. قصة تدعمها (من حقيبة الفيديو، دون أرقام مالية): «حين خالفنا هذه القاعدة مرة وجربنا طريقة جديدة كاملة دون نسخة صغيرة، ضاع جهد ومال. ومنذ ذلك اليوم: أي طريقة جديدة تبدأ صغيرة.» هذا يبني ثقة: قاعدة جربناها بأنفسنا.')

add('workbook', P('الكراسة',34,TEAL,extra='font-weight:700')+H('مهمة واحدة وخمس أوراق ومشروع منجز',60)+
 row(f'<img src="{WB}" alt="صفحة من كراسة أدوات العمل" style="width:620px;height:620px;object-fit:contain;background:#ECE7DA;border-radius:20px">',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:18px;justify-content:center">'+''.join(P(x,34,INK) for x in ['١ بطاقة المهمة','٢ مقارنة أداتين','٣ قالب البرومبت','٤ سجل التنفيذ والتحقق','٥ ملخص المشروع الختامي'])+P('تُكتب على الحاسوب أو الهاتف مباشرة',34,TEAL,extra='font-weight:700')+'</div>'),
 'دقيقة 44 إلى 48. الفكرة: المتدرب لا يحل خمسة تمارين متفرقة، بل يبني مشروعًا واحدًا على مهمة من عمله. في النهاية، الورقة الخامسة وثيقة مشروع كاملة: المهمة، والأداة، والتعليمات، والمخرج، وطريقة التحقق. اذكر أن الكراسة صارت تُكتب على الحاسوب بخانات جاهزة.')

add('inside', H('ماذا تجد داخل الحقيبة؟',72)+
 row(f'<img src="{U1}" alt="صفحة من ملف الوحدة الأولى" style="width:820px;height:461px;object-fit:contain;background:#ECE7DA;border-radius:20px">',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:18px;justify-content:center">'+''.join(P(x,34,INK) for x in ['فيديو قصير لكل وحدة','ملف PDF مصمم للقراءة','امتحان قصير يفتح الوحدة التالية','اختبار قبلي وبعدي','شهادة إتمام'])+'</div>'),
 'دقيقة 48 إلى 52. هنا الجولة في الحقيبة: شغّل فيديو الجولة المسجل مسبقًا (3 دقائق)، أو ادخل منصة CPS بحساب متدرب إن كان الإنترنت مستقرًا. اعرض وحدة واحدة: الفيديو، ثم الملف، ثم الامتحان. احتفظ بالفيديو المسجل جاهزًا احتياطيًا.')

axes=[('الفكرة والعميل','من الخطوة 1 إلى 6'),('المنتج','من الخطوة 7 إلى 9'),('التسويق','من الخطوة 10 إلى 14'),('الإيراد','من الخطوة 15 إلى 17'),('البناء والجودة','من الخطوة 18 إلى 21'),('الإطلاق والاستدامة','من الخطوة 22 إلى 24')]
add('built', P('كيف بنيتها',34,TEAL,extra='font-weight:700')+H('المنهجية الأربع والعشرون',64)+
 grid([card(a,b) for a,b in axes],3)
 +P('من مخيم صناعة المنتج الرقمي: كل قرار في الحقيبة جواب عن سؤال في إحدى هذه الخطوات',34,NAVY),
 'دقيقة 52 إلى 56. هذه الشريحة للزملاء المدربين خصوصًا. اذكر مثالين فقط: الخطوة 2 (العميل): «مستخدم عربي لديه مهمة عملية ولا يعرف الأداة الأنسب»، والخطوة 9 (مخطط المحتوى): «نتيجة تعلم لكل وحدة صاعدة على سلم بلوم». إن سُئلت عن الخطوات الناقصة: «أنجزنا المنتج كاملًا، والسوق خطته مكتوبة ويُقاس بعد النشر.»')

add('ai', H('الذكاء الاصطناعي نفّذ وأنا قررت',72)+
 row(f'<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:{SOFT};border-radius:28px;padding:44px"><h3 style="font-size:42px;color:{TEAL};text-align:right">{r("ما نفّذته الأدوات")}</h3>'+''.join(P(x,32,INK) for x in ['صياغة مسودات المحتوى','التصميم والإخراج','الأسئلة الأولية'])+'</div>',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:{GSOFT};border-radius:28px;padding:44px"><h3 style="font-size:42px;color:{GOLD};text-align:right">{r("ما قررته أنا")}</h3>'+''.join(P(x,32,INK) for x in ['المنهج والجمهور والوعد','ما يبقى وما يُحذف','مراجعة كل وحدة قبل نشرها'])+'</div>'),
 'دقيقة 56 إلى 58. توقّع سؤال الأصالة، فاسبقه بهذه الشريحة. الجملة الأساسية: «الأدوات تنفّذ بسرعة، لكنها لا تعرف جمهوري ولا تقرر عني. كل قرار في الحقيبة مسجل مع سببه.» هذه أيضًا رسالة الحقيبة نفسها: أنت تقرر، والأداة تنفذ.')

add('lessons', H('ثلاث أفكار تأخذها اليوم',72)+
 row(card('المهمة قبل الأداة','صغها في جملة قبل أي بحث','1',accent=GOLD),card('أداتان فقط','قارن بخمسة معايير واختر','2',accent=GOLD),card('نسخة صغيرة أولًا','افحص ثم اعتمد','3',accent=GOLD)),
 'دقيقة 58 إلى 59. لخّص كل المحاضرة في ثلاث جمل. قل: «إن نسيتم كل شيء، تذكروا هذه الثلاث.»')

add('next', H('بعد هذه الحقيبة',72)+
 row(f'<img src="{VC}" alt="غلاف حقيبة مسار الفيديو" style="width:880px;height:495px;object-fit:cover;border-radius:24px">',
     f'<div style="flex:1;display:flex;flex-direction:column;gap:20px;justify-content:center">'+H('مسار الفيديو',56,NAVY,'h3')+P('حقيبة متخصصة بالمنهج نفسه: من بطاقة إلى فيديو منشور، في ست وحدات',34,INK)+P('فيديوهاتها صُنعت بالطريقة التي تعلّمها',34,TEAL,extra='font-weight:700')+'</div>'),
 'دقيقة 59 إلى 60. تمهيد قصير جدًا للحقيبة الثانية، دون بيع مباشر هنا: «لمن يريد التخصص، هذه الحقيبة الثانية، وستكون لها محاضرة خاصة.» إن لم تكن مفعّلة بعد، قل: «قريبًا».')

add('cta', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:28px">'
 +H('ابدأ الآن مجانًا',100,'#FFFFFF','h2')
 +P('[رابط التسجيل في الحقيبة على منصة CPS]',44,'#F2C94C',extra='font-weight:700')
 +P('الرابط في الدردشة الآن',36,'#E8F4F3')
 +P('[ضع رمز QR هنا]',30,'#C9D6E3')+'</div>',
 'دقيقة 60. اطلب من مساعد، أو انسخ بنفسك، رابط التسجيل في الدردشة الآن. قل: «الحقيبة مجانية، وتستطيعون البدء الليلة بمهمة حقيقية من عملكم.» اترك الشريحة ظاهرة 20 ثانية قبل الأسئلة.',
 bg=NAVY,color='#FFFFFF')

add('qa', f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:28px">'
 f'<img src="{LOGO}" alt="شعار مسار" style="width:420px;height:212px;object-fit:contain">'
 +f'<h2 style="font-size:110px;font-weight:700;color:{NAVY};text-align:center">{r("أسئلتكم")}</h2>'
 +f'<p style="font-size:38px;color:{MUTE};text-align:center">{r("اكتبها في الدردشة أو ارفع يدك")}</p></div>',
 'دقيقة 60 إلى 75. اقرأ كل سؤال بصوت مسموع قبل الإجابة. أسئلة الزوار المتوقعة: هل أحتاج خبرة؟ (لا، مهمة حقيقية فقط). هل أحتاج أن أدفع لأدوات؟ (لا، المعايير تشمل الكلفة والبدائل المجانية). كم المدة؟ هل الشهادة معتمدة؟ أسئلة الزملاء: ما الجديد مقارنة بدورات البرومبت؟ (البرومبت الوحدة الرابعة من خمس، والجديد ما قبله وما بعده). كيف تقيس الأثر؟ (اختبار قبلي وبعدي، والمشروع الختامي). ما أصعب ما واجهك؟ («أن أقاوم إغراء تعليم الأدوات»). اختم بشكر الحضور والمنظمين، وأعد الرابط في الدردشة.',
 bg=CREAM)

order=[i for i,_ in S]
for i,h in S: open(f'{ROOT}/slides/{i}.html','w',encoding='utf-8').write(h)
deck={"v":4,"createdOnFiles":{"v":1,"at":datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},"lists":"css","title":"محاضرة: مسار الذكاء الاصطناعي — من التشتت إلى قرار","order":order,
 "sections":{"s1":{"description":"الافتتاح والمشكلة","start":"cover"},"s2":{"description":"الطريق وتطبيقه حيًا","start":"package"},"s3":{"description":"داخل الحقيبة وكيف بُنيت","start":"workbook"},"s4":{"description":"الختام والدعوة والأسئلة","start":"lessons"}},
 "cover":"cover","faces":{"amiri":{"family":"Amiri","href":"https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap"}},"designSystems":[]}
json.dump(deck,open(f'{ROOT}/deck.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(order),order)
