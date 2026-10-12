"""تجميع صوت الإعلان وكتابة spec.json (المسودة: draft-*.mp4، والنهائي: presenter-*.mp4 بتمرير final)."""
import json,subprocess,re,os,sys
D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D); FINAL='final' in sys.argv
v={c['output']:c['text'] for c in json.load(open('voice.json',encoding='utf-8'))['clips']}
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode())
plain=lambda t: re.sub('[\u064B-\u0652]','',t)
def build(name,groups,lead=0.25,hold=1.0,gap=0.45,step=0.0):
    parts=[];t=0;starts={};scenes=[]
    def sil(d):
        nonlocal t
        if d<=0.001: return
        f=f'/tmp/psil_{len(parts)}.wav'; subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t',f'{d:.3f}',f]); parts.append(f); t+=d
    for g,st in groups:
        s0=t; sil(lead); prev=None
        for sid in g:
            w=f'/tmp/p_{sid}.wav'; subprocess.run(['ffmpeg','-v','error','-y','-i',f'seg-{sid}.mp3','-ar','44100','-ac','1',w])
            if prev: sil(max(gap, (prev[0]+st)-t) if st else gap)
            starts[sid]=t; parts.append(w); d=dur(w); prev=(t,d); t+=d
        sil(hold); scenes.append((round(s0,2),round(t,2)))
    open('/tmp/pcat.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','/tmp/pcat.txt','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','44100','-b:a','160k',name])
    return scenes,starts
O,so=build('narration-open.mp3',[(['p1','p2'],0)],hold=0.6)
S,sc=build('narration-cards.mp3',[(['g1','g2','g3','g4','g5','g6'],2.15),(['c1','c2','c3'],0)],lead=0.8,hold=1.2)
C,scl=build('narration-close.mp3',[(['cl0','cl1'],0)],hold=0.8)
r=lambda x:round(max(x,0.2),2)
cap=lambda st,ids:[[round(st[i],2),round(st[i]+dur(f'seg-{i}.mp3'),2),plain(v[f'seg-{i}.mp3'])] for i in ids]
pre='presenter' if FINAL else 'draft'
units=['البطاقة','النص','الصوت','الصورة','المونتاج','النشر']
segs=[{"type":"presenter","video":f"{pre}-open.mp4","audio":{"file":"narration-open.mp3"},"screen":{"kicker":"حقيبة مسار الفيديو","title":"أنتج الفيديو<br>[[الخاص بك]]","button":"ست وحدات · من بطاقة إلى فيديو منشور","reveal_at":[r(so['p2']-0.1)]},"captions":cap(so,['p1','p2'])},
 {"type":"card","audio":{"file":"narration-cards.mp3","start":S[0][0],"end":S[0][1]},"card":{"kind":"thumbs","title":"[[ست]] وحدات","cols":3,"items":[[n,f"publish/youtube/unit-{i+1}.jpg"] for i,n in enumerate(units)],"reveal_at":[r(sc[f'g{k}']-S[0][0]-0.1) for k in range(1,7)]}},
 {"type":"card","audio":{"file":"narration-cards.mp3","start":S[1][0],"end":S[1][1]},"card":{"kind":"cards","title":"في كل [[وحدة]]","items":[["فيديو قصير","يشرح ويُري","green"],["ملف وورقة عمل","تطبّق فيها","green"],["برومبت جاهز","وأدوات مع بديل مجاني","amber"]],"reveal_at":[r(sc[k]-S[1][0]-0.1) for k in ('c1','c2','c3')]}},
 {"type":"presenter","video":f"{pre}-close.mp4","audio":{"file":"narration-close.mp3"},"screen":{"kicker":"سجّل الآن","title":"من بطاقة إلى<br>[[فيديو منشور]]","lines":["هذا الإعلان صُنع بالطريقة نفسها"],"foot":"حقيبة مسار الفيديو · منصة مسار","reveal_at":[r(scl['cl0']-0.1),r(scl['cl1']-0.1)]},"captions":cap(scl,['cl0','cl1'])},
 {"type":"end","title":"مسار [[الفيديو]]","sub":"حقيبة تدريبية من منصة مسار","duration":3.0}]
spec={"title":"إعلان حقيبة مسار الفيديو","theme":"video","label":"حقيبة مسار الفيديو","output":"masar-video-promo.mp4" if FINAL else "masar-video-promo-draft.mp4","crossfade":0.4,"screen_box":[562,27,1280,534],"segments":segs}
json.dump(spec,open('spec.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for n in ('narration-open.mp3','narration-cards.mp3','narration-close.mp3'): print(n,round(dur(n),2))
print('scenes',S,'thumbs',segs[1]['card']['reveal_at'],'cards',segs[2]['card']['reveal_at'])
