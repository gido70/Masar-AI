"""تحضير المسودة الصامتة للوحدة 0: صوت كل مشهد من مقاطعه، وصوت المشهد 1 (موسيقى مبهرة + test-0a)،
وفيديو سراج الثابت، ثم كتابة spec.json بتوقيتات الظهور المحسوبة. التشغيل من جذر المستودع:
    python productions/ads-unit-0/prep_draft.py"""
import json, os, subprocess, re
B = os.path.dirname(os.path.abspath(__file__)); J = lambda x: os.path.join(B, x)
GAP = 0.45
def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode())
def concat(parts, out, lead=0.3):
    """يضم المقاطع بفواصل ثابتة ويعيد زمن بداية كل مقطع."""
    starts, t, inp, fl = [], lead, [], []
    for k, p in enumerate(parts):
        inp += ['-i', J(p)]; starts.append(round(t, 2)); d = dur(J(p))
        fl.append(f'[{k}:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(t*1000)}|{int(t*1000)},apad=whole_dur={t+d+0.05:.3f}[a{k}]')
        t += d + GAP
    fl.append(''.join(f'[a{k}]' for k in range(len(parts))) + f'amix=inputs={len(parts)}:normalize=0:duration=longest[o]')
    ff(*inp, '-filter_complex', ';'.join(fl), '-map', '[o]', J(out)); return starts, round(t - GAP, 2)

# المشهد 1: موسيقى مبهرة 9 ث بانقطاع حاد + «سَمَر… الطعم الأسطوري» عند 6.2 ث
ff('-i', J('music-flashy.mp3'), '-i', J('test-0a.mp3'), '-filter_complex',
   '[0:a]atrim=0:8.85,afade=t=in:d=0.3,volume=0.55,apad=whole_dur=9[m];[1:a]adelay=6200|6200,volume=1.6[v];[m][v]amix=inputs=2:normalize=0:duration=first,aformat=channel_layouts=mono[o]',
   '-map', '[o]', '-ar', '44100', J('scene1.wav'))
s3, e3 = concat(['seg-c3_1.mp3','seg-c3_2.mp3','seg-c3_3.mp3','seg-c3_4.mp3'], 'scene3.wav', lead=0.6)
s4a, e4a = concat(['seg-c4_1.mp3','seg-c4_2.mp3'], 'scene4a.wav')
s4b, e4b = concat(['seg-c4_3.mp3','seg-c4_4.mp3'], 'scene4b.wav')
s5, e5 = concat(['seg-c5_0.mp3','seg-c5_1.mp3','seg-c5_2.mp3','seg-c5_3.mp3','seg-c5_4.mp3'], 'scene5.wav', lead=0.6)

# سراج ثابت (للمسودة فقط): الصورة الطولية فوق خلفيتها المموّهة، مع تقريب بطيء
img = os.path.join(B, '..', '..', 'studio', 'assets', 'siraj-ref-desk.png')
ff('-loop', '1', '-i', img, '-filter_complex',
   '[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.08[bg];'
   '[0:v]scale=-2:1080[fg];[bg][fg]overlay=260:0,zoompan=z=\'min(1+0.0004*on,1.08)\':d=1:s=1920x1080:fps=25,format=yuv420p[o]',
   '-map', '[o]', '-t', '20', '-c:v', 'libx264', '-crf', '20', J('presenter-still.mp4'))

def caps(audio, lines):
    """توقيت الشرح بتوزيع مدة الكلام على الجمل حسب طولها (للمسودة)."""
    d = dur(J(audio)) - 0.1; L = [len(x) for x in lines]; t = 0.15; out = []
    for x, l in zip(lines, L):
        w = (d - 0.15) * l / sum(L); out.append([round(t, 2), round(t + w - 0.1, 2), x]); t += w
    return out

do, dc = dur(J('narration-open.mp3')), dur(J('narration-close.mp3'))
SYNC = os.path.exists(J('presenter-open.mp4'))  # سراج المتحرك المتزامن إن وُجد، وإلا الصورة الثابتة
OPEN_V, OPEN_A, LEAD = ('presenter-open.mp4', 'narration-open-pad.mp3', 0.5) if SYNC else ('presenter-still.mp4', 'narration-open.mp3', 0.0)
spec = {
 "title": "صناعة الإعلانات · الوحدة 0: الفكرة قبل الأداة", "theme": "ads",
 "label": "صناعة الإعلانات · الوحدة 0: الفكرة قبل الأداة", "output": "ads-unit-0-draft.mp4", "crossfade": 0.4,
 "music": {"file": "music-B-modern.mp3", "from_segment": 3, "speech_db": -15, "gap_db": -6, "down": 1.5, "up": 2.0, "fade_in": 1.5, "fade_out": 2.5},
 "segments": [
  {"type": "broll", "video": "broll-1a.mp4", "hold": 0, "audio": {"file": "scene1.wav", "start": 0.0, "end": 3.0}},
  {"type": "broll", "video": "broll-1b.mp4", "hold": 0, "audio": {"file": "scene1.wav", "start": 3.0, "end": 6.0}},
  {"type": "broll", "video": "broll-1c.mp4", "hold": 0, "audio": {"file": "scene1.wav", "start": 6.0, "end": 9.0},
   "overlay_style": "flashy", "overlay_at": 0.2, "overlay": {"title": "سَمَر… الطعم الأسطوري"}},
  {"type": "broll", "video": OPEN_V, "no_stretch": True, "overlay_pos": "top", "overlay_at": 0.8,
   "audio": {"file": OPEN_A, "start": 0.0, "end": round(dur(J(OPEN_A)), 2)}, "hold": 0.3 if OPEN_V == "presenter-open.mp4" else 1.2,
   "overlay": {"kicker": "صناعة الإعلانات · الوحدة 0", "title": "الفكرة [[قبل الأداة]]", "text": "إعلان أداة… أم إعلان فكرة؟"},
   "overlay_width": 640, "overlay_right": 60,
   "captions": [[a + LEAD, b + LEAD, x] for a, b, x in caps('narration-open.mp3', ["جميل… لكن ماذا قال؟", "يبهر العين… ثم يُنسى.", "هذا إعلان أداة."])]},
  {"type": "card", "audio": {"file": "scene3.wav", "start": 0.0, "end": round(e3 + 0.4, 2)}, "hold": 1.0,
   "card": {"kind": "compare", "title": "[[أداة]] أم فكرة؟",
    "before": {"label": "إعلان الأداة", "text": "يبدأ من المؤثرات", "verdict": "بعده يسأل المشاهد: ماذا رأيت؟", "quote": False},
    "after": {"label": "إعلان الفكرة", "text": "يبدأ من رسالة واحدة", "verdict": "بعده يسأل: ماذا فهمت؟", "quote": False},
    "reveal_at": s3}},
  {"type": "broll", "video": "broll-4a.mp4", "audio": {"file": "scene4a.wav", "start": 0.0, "end": e4a}, "overlay_at": max(s4a[1] - 0.2, 0.3),
   "overlay": {"kicker": "نفس القهوة… بفكرة واحدة", "title": "الرسالة: [[سَمَر تجمع الناس]]"}},
  {"type": "broll", "video": "broll-4b-crop.mp4", "audio": {"file": "scene4b.wav", "start": 0.0, "end": e4b}, "hold": 1.5, "overlay_at": 0.3,
   "overlay": {"kicker": "الرمز", "title": "فنجانٌ يُصب… [[فيمتلئ المجلس]]"}},
  {"type": "card", "audio": {"file": "scene5.wav", "start": 0.0, "end": e5}, "hold": 1.5,
   "card": {"kind": "tree", "title": "[[اختبار]] الفكرة",
    "rows": [["رسالتك", "في جملة واحدة؟"], ["احذف المؤثرات", "هل بقيت الفكرة؟"], ["المشاهد", "هل يتذكره غدًا؟"]],
    "note": "<b style=\"color:#B0186A\">القاعدة:</b><br>الأداة تنفّذ<br>والفكرة تقنع", "reveal_at": s5[1:]}},
  {"type": "broll", "video": "presenter-still.mp4", "no_stretch": True, "overlay_pos": "top", "overlay_at": 0.8,
   "audio": {"file": "narration-close.mp3", "start": 0.0, "end": round(dc, 2)}, "hold": 1.2,
   "overlay": {"kicker": "مهمتك الآن", "title": "افحص [[ثلاثة إعلانات]]", "text": "شاهد · اسأل الأسئلة الثلاثة<br>صنّف: أداة أم فكرة؟"},
   "overlay_width": 640, "overlay_right": 60,
   "captions": caps('narration-close.mp3', ["مهمتك الآن: شاهد ثلاثة إعلانات اليوم،", "واسأل عن كل واحد الأسئلة الثلاثة…", "ثم صنّفه: أداة أم فكرة؟", "وفي الوحدة الأولى، نبدأ من أول الطريق: الموجز."])},
  {"type": "end", "title": "صناعة [[الإعلانات]]", "sub": "التالي: الوحدة 1 · الموجز والبصيرة", "duration": 3.0}]}
json.dump(spec, open(J('spec-draft.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('scene3', s3, e3, '| 4a', s4a, e4a, '| 4b', s4b, e4b, '| scene5', s5, e5)
