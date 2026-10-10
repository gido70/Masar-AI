# مصنع فيديو مسار (المرحلة 1)

ينتج فيديو كاملًا من ملف وصف واحد: البطاقات، والظهور التدريجي، وتركيب المحتوى على شاشة المقدّم، والترجمة النصية، والمونتاج، والصوت.

## التشغيل
```bash
pip install -r studio/requirements.txt
python -m playwright install chromium     # مرة واحدة
python studio/make_video.py productions/<اسم-الفيديو>/spec.json
```
المتطلبات: Python 3 و ffmpeg. المشاهد المنتَجة تُحفظ في `_work/` وتُعاد استخدامها؛ لإعادة إنتاج كل شيء: `FORCE=1`.

## إنتاج فيديو جديد
1. أنشئ مجلدًا: `productions/<اسم>/`.
2. ضع فيه: الصوت الكامل (بصوت George)، ومقاطع المقدّم من InfiniteTalk إن وجدت.
3. اكتب `spec.json` (انظر `productions/video-unit-1/spec.json` مثالًا).
4. شغّل المصنع.

## ملف الوصف (spec.json)
| الحقل | المعنى |
|---|---|
| `label` | اسم الحقيبة والوحدة أعلى البطاقات |
| `audio` | أجزاء الصوت بالترتيب: `file` ومعه `start`/`end` اختياريًا |
| `segments` | المشاهد بالترتيب |

**أنواع المشاهد:**
- `presenter`: فيديو المقدّم (`video`) + محتوى الشاشة (`screen`: `kicker`، `title`، `lines`، `button`، `foot`) + `captions` بتوقيت داخل المقطع.
- `card` + `duration` + `card`:
  - `grid`: عناصر مرقّمة `items: [[عنوان, شرح], ...]`، و`cols`.
  - `tree`: صفوف «غرض ← شكل» `rows`، و`note` جانبية.
  - `rule_bars`: لافتة قاعدة `rule {big, text, note}` + أشرطة `bars: [[اسم, قيمة, نسبة 0–1], ...]`.
  - `cards`: بطاقات ملونة `items: [[عنوان, قيمة, green|amber|red], ...]` + `warning`.
- `end`: بطاقة الختام `title`، `sub`، `duration`.

`[[كلمة]]` في أي عنوان تُلوَّن بلون التأكيد. عناصر كل بطاقة تظهر تدريجيًا على مدة المشهد.

## قواعد مجرّبة
- مدة كل مشهد بطاقة = المسافة بين وقفات الصوت (استخرجها من `silences()` في الملف).
- مقاطع المقدّم تُقص من الصوت الكامل عند الوقفات، وتُرفع إلى InfiniteTalk على `studio/assets/presenter-screen.png`.
- الهوية في `THEMES` داخل `make_video.py`؛ كل حقيبة يمكن أن تضيف هويتها.
