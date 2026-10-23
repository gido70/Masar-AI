"""مسودة الوحدة 1 (وبعد وصول لقطتي سراج: النسخة النهائية). التشغيل من جذر المستودع:
    python productions/ads-unit-1/prep_draft.py  ثم  python studio/make_video.py productions/ads-unit-1/spec-draft.json"""
import json, os, subprocess
B = os.path.dirname(os.path.abspath(__file__)); J = lambda x: os.path.join(B, x)
def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
def dur(p): return round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode()), 2)

# كلام سراج قصير ونظيف (≤ 5 ث): لقطات Flow مدتها 10 ث، والورقة تختفي فيها اختفاءً غير طبيعي، فنأخذ الجزء النظيف فقط (سجل 246)
def cut(src, out, a, b=None, fade=True):
    args = ['-ss', str(a), '-i', J(src)] + (['-t', str(round(b - a, 2))] if b else [])
    if fade and b: args += ['-af', 'afade=t=out:st=%.2f:d=0.12' % (b - a - 0.12)]
    ff(*args, J(out))
cut('narration-open.mp3', 'narration-open-1.mp3', 0, 3.62)        # «هذه ليست طلبًا… هذه بداية سؤال.» على سراج
cut('narration-open.mp3', 'narration-open-2.mp3', 4.0, None)      # «وفي هذه الوحدة…» فوق بطاقة
cut('narration-close.mp3', 'narration-close-a1.mp3', 0, 4.47)     # «مهمتك الآن: … أرسل لك رسالته.» على سراج
cut('narration-close.mp3', 'narration-close-a2.mp3', 5.0, 11.68)  # الخطوات الثلاث فوق بطاقة المهمة
cut('narration-close.mp3', 'narration-close-b.mp3', 12.0, None)   # «وفي الوحدة الثانية…» فوق بطاقة الختام
def pad(n, lead, tail):
    ff('-f', 'lavfi', '-t', str(lead), '-i', 'anullsrc=r=44100:cl=mono', '-i', J(n + '.mp3'), '-f', 'lavfi', '-t', str(tail), '-i', 'anullsrc=r=44100:cl=mono',
       '-filter_complex', '[1:a]aresample=44100,aformat=channel_layouts=mono[v];[0:a][v][2:a]concat=n=3:v=0:a=1[o]', '-map', '[o]', J(n + '-pad.mp3'))
pad('narration-open-1', 0.4, 0.5); pad('narration-close-a1', 0.22, 0.2)
# الأساس الصامت لمزامنة الشفاه: الجزء النظيف من لقطتي Flow (بعد اختفاء الورقة)
for src, start, aud, out in (('flow-raw-C.mp4', 3.0, 'narration-open-1-pad.mp3', 'base-open.mp4'), ('flow-raw-A.mp4', 4.0, 'narration-close-a1-pad.mp3', 'base-close.mp4')):
    if not os.path.exists(J(out)):
        ff('-ss', str(start), '-i', J(src), '-t', str(dur(J(aud)) + 0.3), '-an', '-vf', 'scale=1280:720', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', J(out))
if not os.path.exists(J('presenter-still.mp4')):
    img = os.path.join(B, '..', '..', 'studio', 'assets', 'avatars', 'siraj.png')
    ff('-loop', '1', '-i', img, '-filter_complex',
       '[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.08[bg];'
       '[0:v]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2+380:0,format=yuv420p[o]', '-map', '[o]', '-t', '20', '-r', '25', '-c:v', 'libx264', '-crf', '20', J('presenter-still.mp4'))

def stretch(src, out, cuts):
    """يضيف صمتًا (ثوانٍ) داخل وقفات طبيعية في الكلام، دون إعادة توليد الصوت. cuts = [(موضع داخل الوقفة, صمت إضافي)]"""
    pts = [0.0] + [c for c, _ in cuts] + [None]; fl = []; n = 0
    for k in range(len(pts) - 1):
        a, b = pts[k], pts[k + 1]
        fl.append(f"[0:a]atrim=start={a}" + (f":end={b}" if b else '') + f",asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono[p{n}]"); n += 1
        if k < len(cuts):
            fl.append(f"anullsrc=r=44100:cl=mono,atrim=0:{cuts[k][1]}[p{n}]"); n += 1
    fl.append(''.join(f'[p{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1[o]')
    ff('-i', J(src), '-filter_complex', ';'.join(fl), '-map', '[o]', J(out))

# تعداد الأسئلة الخمسة والمعادلة: وقفات أطول ليُقرأ كل عنصر (ملاحظة الإيقاع في المسودة الأولى)
stretch('n-s4.mp3', 'n-s4x.mp3', [(5.08, 0.8), (6.2, 0.8), (9.5, 0.8), (11.45, 0.8)])
stretch('n-s8.mp3', 'n-s8x.mp3', [(1.47, 0.5), (2.32, 0.6), (3.48, 0.4), (7.2, 0.5)])

def caps(audio, lines, lead=0.0, tail=0.0):
    d = dur(J(audio)) - 0.1 - tail; L = [len(x) for x in lines]; t = 0.15 + lead; out = []
    for x, l in zip(lines, L):
        w = (d - 0.15 - lead) * l / sum(L); out.append([round(t, 2), round(t + w - 0.1, 2), x]); t += w
    return out

SO, SC = os.path.exists(J('presenter-open.mp4')), os.path.exists(J('presenter-close.mp4'))
OV, OA, OL = ('presenter-open.mp4', 'narration-open-1-pad.mp3', 0.4) if SO else ('presenter-still.mp4', 'narration-open-1.mp3', 0.0)
CV, CA, CL = ('presenter-close.mp4', 'narration-close-a1-pad.mp3', 0.22) if SC else ('presenter-still.mp4', 'narration-close-a1.mp3', 0.0)
A = lambda f: {"file": f, "start": 0.0, "end": dur(J(f))}
spec = {
 "title": "صناعة الإعلانات · الوحدة 1: الموجز والبصيرة", "theme": "ads",
 "label": "صناعة الإعلانات · الوحدة 1: الموجز والبصيرة", "output": "ads-unit-1-final.mp4" if (SO and SC) else "ads-unit-1-draft.mp4", "crossfade": 0.4,
 "music": {"file": "../ads-unit-0/music-B-modern.mp3", "from_segment": 0, "speech_db": -12, "gap_db": -4, "down": 1.5, "up": 2.0, "merge": 0.8, "fade_in": 1.5, "fade_out": 2.5, "loudnorm": -16},
 "segments": [
  {"type": "broll", "video": "broll-1.mp4", "audio": A("n-s1.mp3"), "hold": 0.6, "overlay_at": 2.3,
   "overlay": {"kicker": "رسالة من عميل", "title": "«أريد إعلانًا لقهوتي… [[يكون جميلًا]]»"}},
  {"type": "broll", "video": OV, "no_stretch": True, "overlay_pos": "top", "overlay_at": 0.8, "audio": A(OA), "hold": 0.3,
   "overlay": {"kicker": "صناعة الإعلانات · الوحدة 1", "title": "الموجز [[والبصيرة]]", "text": "من رسالة مبهمة إلى صفحة واحدة"},
   "overlay_width": 640, "overlay_right": 60,
   "captions": [[a + OL, b + OL, x] for a, b, x in caps('narration-open-1.mp3', ["هذه ليست طلبًا… هذه بداية سؤال."])]},
  {"type": "card", "audio": A("narration-open-2.mp3"), "hold": 1.0,
   "card": {"kind": "cards", "title": "ماذا تتعلم في [[هذه الوحدة]]؟",
    "items": [["الرسالة المبهمة", "تتحوّل إلى…", "red"], ["موجز", "من صفحة واحدة", "green"], ["بصيرة", "في جملة", "amber"]],
    "reveal_at": [0.3, 3.3, 5.82]}},
  {"type": "card", "audio": A("n-s3.mp3"), "hold": 2.1,
   "card": {"kind": "compare", "title": "طلب [[مبهم]] أم موجز؟",
    "before": {"label": "طلب مبهم", "text": "أريد إعلانًا جميلًا", "verdict": "تخمين… وتعديلات لا تنتهي"},
    "after": {"label": "موجز", "text": "صفحة واحدة: من نخاطب، وماذا نقول، ولماذا يصدقنا", "verdict": "الجميع يرى الهدف نفسه"},
    "reveal_at": [0.3, 2.45, 6.8, 9.2]}},
  {"type": "card", "audio": A("n-s4x.mp3"), "hold": 1.2,
   "card": {"kind": "grid", "title": "أسئلة العميل [[الخمسة]]", "cols": 5,
    "items": [["ماذا تبيع؟"], ["لمن؟"], ["ماذا يفعل الناس بعده؟"], ["لماذا يصدقونك؟"], ["أين ومتى وبكم؟"]],
    "reveal_at": [4.07, 6.18, 8.16, 12.13, 14.98]}},
  {"type": "card", "audio": A("n-s5.mp3"), "hold": 1.2,
   "card": {"kind": "tree", "title": "ورقة [[الموجز]]",
    "rows": [["من نخاطب؟", "شباب يجتمعون كل مساء"], ["ماذا نقول؟", "رسالة واحدة"], ["لماذا يصدقنا؟", "تُحمَّص طازجة كل أسبوع"]],
    "note": "<b style=\"color:#B0186A\">الدليل:</b><br>دليل واحد<br>يكفي", "reveal_at": [2.83, 8.73, 11.78, 15.35]}},
  {"type": "broll", "video": "broll-6-crop.mp4", "audio": A("n-s6.mp3"), "hold": 1.0, "overlay_at": 5.0,
   "overlay": {"kicker": "انظر إلى هذا المجلس", "title": "خمسة معًا… [[وكل واحد في هاتفه]]"}},
  {"type": "card", "audio": A("n-s7.mp3"), "hold": 2.4,
   "card": {"kind": "compare", "title": "معلومة أم [[بصيرة]]؟",
    "before": {"label": "معلومة", "text": "الشباب يحبون القهوة", "verdict": "يعرفها الجميع… ولا تحرك أحدًا"},
    "after": {"label": "بصيرة", "text": "نجتمع كل مساء… لكن لا نلتقي", "verdict": "حقيقة يعيشها الجمهور ولا يقولها"},
    "reveal_at": [3.76, 6.15, 10.72, 12.4]}},
  {"type": "card", "audio": A("n-s8x.mp3"), "hold": 1.5,
   "card": {"kind": "rule_bars", "title": "معادلة [[البصيرة]]",
    "rule": {"big": "=", "text": "<b>حقيقة + لكن</b><br>= بصيرة", "note": ""},
    "bars": [["حقيقة", "أولًا", 0.45], ["ثم: لكن", "ثانيًا", 0.65], ["الاختبار", "«صدقتَ… هذا نحن»", 0.9]],
    "reveal_at": [0.3, 2.16, 3.53, 9.37]}},
  {"type": "card", "audio": A("n-s9.mp3"), "hold": 1.2,
   "card": {"kind": "cards", "title": "من البصيرة إلى [[الرسالة]]",
    "items": [["البصيرة", "نجتمع ولا نلتقي", "amber"], ["الرسالة", "سَمَر تجمع الناس", "green"], ["الذكاء الاصطناعي", "يقترح… والاختيار لك", "red"]],
    "reveal_at": [0.3, 2.48, 4.38]}},
  {"type": "broll", "video": CV, "no_stretch": True, "overlay_pos": "top", "overlay_at": 0.8, "audio": A(CA), "hold": 0.3,
   "overlay": {"kicker": "مهمتك الآن", "title": "موجز [[«سنابل»]]"},
   "overlay_width": 640, "overlay_right": 60,
   "captions": [[a + CL, b + CL, x] for a, b, x in caps('narration-close-a1.mp3', ["مهمتك الآن: صاحب مخبز سنابل أرسل لك رسالته."])]},
  {"type": "card", "audio": A("narration-close-a2.mp3"), "hold": 1.5,
   "card": {"kind": "cards", "title": "مهمتك: موجز [[«سنابل»]]",
    "items": [["① اقرأ", "إجاباته عن الأسئلة الخمسة", "green"], ["② اكتب", "موجزه في صفحة واحدة", "amber"], ["③ اختر", "بصيرة فيها «لكن»", "red"]],
    "reveal_at": [0.3, 3.0, 4.88]}},
  {"type": "end", "title": "الموجز [[والبصيرة]]", "sub": "التالي: الوحدة 2 · محرّك الأفكار",
   "audio": A("narration-close-b.mp3"), "duration": round(dur(J('narration-close-b.mp3')) + 1.8, 2),
   "captions": caps('narration-close-b.mp3', ["وفي الوحدة الثانية… نحوّل موجزك إلى عشرين فكرة."])}]}
json.dump(spec, open(J('spec-draft.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: dur(J(k)) for k in ('narration-open-1-pad.mp3','narration-open-2.mp3','narration-close-a1-pad.mp3','narration-close-a2.mp3','narration-close-b.mp3','base-open.mp4','base-close.mp4')})
