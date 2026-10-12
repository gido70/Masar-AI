import json,subprocess,re,os
D='/home/claude/Masar-AI/productions/video-unit-6'; os.chdir(D)
v={c['output']:c['text'] for c in json.load(open('voice.json',encoding='utf-8'))['clips']}
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
def plain(t): return re.sub('[\u064B-\u0652]','',t)
GAP=0.45
def build(name, groups, lead=0.25, hold=1.2):
    """groups: list of scenes, each list of seg ids. returns per-scene (start,end) and per-seg start (absolute)."""
    parts=[];t=0;starts={};scenes=[]
    def sil(d):
        nonlocal t; f=f'/tmp/sil_{len(parts)}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t',f'{d:.3f}',f]); parts.append(f); t+=d
    for g in groups:
        s0=t; sil(lead)
        for i,sid in enumerate(g):
            f=f'seg-{sid}.mp3'; starts[sid]=t; w=f'/tmp/{sid}.wav'
            subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-ar','44100','-ac','1',w]); parts.append(w); t+=dur(w)
            if i<len(g)-1: sil(GAP)
        sil(hold); scenes.append((round(s0,2),round(t,2)))
    open('/tmp/cat.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','/tmp/cat.txt','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','44100','-b:a','160k',name])
    return scenes,starts
O,so=build('narration-open.mp3',[['o1','o2','o3']],hold=0.8)
G=[['c2_0','c2_1','c2_2','c2_3','c2_4','c2_5'],['c3_0','c3_1','c3_2','c3_3'],['c4_0','c4_1','c4_2','c4_3'],['c5_0','c5_1','c5_2'],['c6_0','c6_1','c6_2','c6_3'],['c7_0','c7_1','c7_2','c7_3','c7_4']]
S,sc=build('narration-cards.mp3',G,lead=0.6,hold=1.3)
C,scl=build('narration-close.mp3',[['cl0','cl1','cl2','cl3','cl4']],hold=0.8)
r=lambda x:round(max(x,0.2),2)
def rv(scene_i, ids): s0=S[scene_i][0]; return [r(sc[i]-s0-0.1) for i in ids]
cap=lambda st,ids: [[round(st[i],2),round(st[i]+dur(f'seg-{i}.mp3'),2),plain(v[f'seg-{i}.mp3'])] for i in ids]
A=lambda i:{"file":"narration-cards.mp3","start":S[i][0],"end":S[i][1]}
segs=[
 {"type":"presenter","video":"presenter-open.mp4","audio":{"file":"narration-open.mp3"},"screen":{"kicker":"مسار الفيديو · الوحدة 6","title":"التحقق<br>[[والنشر]]","button":"آخر خطوة: النشر على يوتيوب","reveal_at":[r(so['o2']-0.1)]},"captions":cap(so,['o1','o2','o3'])},
 {"type":"card","audio":A(0),"card":{"kind":"grid","title":"افحصه على [[الهاتف]]","cols":5,"items":[["بسماعة","الكلام واضح"],["بلا صوت","الترجمة تكفي"],["الأطراف","النص بعيد عنها"],["الأسماء والأرقام","من نصك"],["مشاهد واحد","يقول الرسالة"]],"reveal_at":rv(0,['c2_1','c2_2','c2_3','c2_4','c2_5'])}},
 {"type":"card","audio":A(1),"card":{"kind":"compare","title":"لا تفعل هذا: [[العنوان]]","before":{"label":"✗ لا تفعل","text":"فيديو جديد، الحلقة الثانية","verdict":"لا يعد بشيء"},"after":{"label":"✓ افعل","text":"اصنع فيديو تعليميًا في ست خطوات","verdict":"وعد واضح وكلمة يبحث عنها جمهورك"},"reveal_at":rv(1,['c3_0','c3_1','c3_2','c3_3'])}},
 {"type":"card","audio":A(2),"card":{"kind":"compare","title":"لا تفعل هذا: [[الصورة المصغرة]]","before":{"label":"✗ لا تفعل","img":"productions/video-unit-6/thumb-dont.jpg","verdict":"لا تُقرأ على الهاتف"},"after":{"label":"✓ افعل","img":"publish/youtube/unit-5.jpg","verdict":"تُقرأ في ثانية"},"reveal_at":rv(2,['c4_0','c4_1','c4_2','c4_3'])}},
 {"type":"card","audio":A(3),"card":{"kind":"cards","title":"[[الوصف]] والفصول","items":[["أول سطرين","الوعد والفائدة","green"],["الفصول","شروط يوتيوب: 0:00 · ثلاثة · 10 ثوانٍ","amber"],["الروابط","السابق والتالي","green"]],"reveal_at":rv(3,['c5_0','c5_1','c5_2'])}},
 {"type":"card","audio":A(4),"card":{"kind":"cards","title":"قبل زر [[النشر]]","items":[["موافقة مكتوبة","لكل من يظهر","red"],["إفصاح","عن المحتوى المولّد الواقعي","amber"],["التراخيص","محفوظة في المشروع","green"]],"warning":"<b style=\"color:#D62828\">على يوتيوب: انشره «غير مدرج» أولًا</b>، وشاهده من الرابط، ثم اجعله عامًا","reveal_at":rv(4,['c6_0','c6_1','c6_2','c6_3'])}},
 {"type":"card","audio":A(5),"card":{"kind":"tree","title":"بطاقة [[القرار]]","rows":[["الخطة","هل وصلت رسالتك؟"],["التكلفة","المتوقعة والفعلية"],["ما نجح","كرّره"],["ما تودّ تغييره","في الفيديو القادم"]],"reveal_at":rv(5,['c7_1','c7_2','c7_3','c7_4'])}},
 {"type":"presenter","video":"presenter-close.mp4","audio":{"file":"narration-close.mp3"},"screen":{"kicker":"مهمتك الآن","title":"انشر [[الفيديو]]<br>الخاص بك","lines":["① افحصه على الهاتف","② انشره على يوتيوب: غير مدرج ثم عام","③ اكتب بطاقة القرار"],"foot":"أكملت حقيبة مسار الفيديو","reveal_at":[r(scl[i]-0.1) for i in ['cl1','cl2','cl3','cl4']]},"captions":cap(scl,['cl0','cl1','cl2','cl3','cl4'])},
 {"type":"end","title":"مسار [[الفيديو]]","sub":"من بطاقة إلى فيديو منشور","duration":3.0}]
spec={"title":"مسار الفيديو · الوحدة 6: التحقق والنشر","theme":"video","label":"مسار الفيديو · الوحدة 6: التحقق والنشر","output":"video-unit-6.mp4","crossfade":0.4,"screen_box":[562,27,1280,534],"segments":segs}
json.dump(spec,open('spec.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for n in ('narration-open.mp3','narration-cards.mp3','narration-close.mp3'): print(n,round(dur(n),2))
print('scenes',S)
for x in segs[1:7]: print(x['card']['kind'],x['card']['reveal_at'])
print('open',segs[0]['screen']['reveal_at'],'close',segs[7]['screen']['reveal_at'])
