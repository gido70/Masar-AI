#!/usr/bin/env python3
"""توليد مقطع فيديو واحد بنموذج Veo 3.1 عبر Gemini API (رصيد الدفع المسبق).

الضوابط الإلزامية لحماية الرصيد:
- فيديو واحد فقط في كل تشغيل (number_of_videos = 1).
- دقة 720p دائمًا، وأقل مدة يسمح بها Veo 3.1 هي 4 ثوانٍ (المدد المتاحة 4 و6 و8).
- نسخة Lite أو Fast فقط (Standard ممنوعة هنا لأنها أغلى بأربع إلى ثماني مرات).
- يرفض التشغيل إن تجاوزت التكلفة التقديرية MAX_COST.
- يرفض إن كان ملف المخرج موجودًا (لا توليد مكرر بالخطأ).
- المفتاح من متغير البيئة GEMINI_API_KEY فقط.
"""
import os, sys, time, mimetypes
from google import genai
from google.genai import types

MODELS = {  # الاسم المختصر: (معرّف النموذج، دولار للثانية بدقة 720p مع الصوت)
    'lite': ('veo-3.1-lite-generate-preview', 0.05),
    'fast': ('gemini-omni-1.1-flash', 0.10),  # Veo 3.1 Fast أُوقف في Gemini API (سجل 259)؛ Omni بالسعر نفسه تقريبًا عند 720p
}
OMNI_MAX_SECONDS = 10  # Omni لا يقبل مدة صريحة؛ نحسب السقف على أطول مقطع ممكن
DURATIONS = (4, 6, 8)
TIMEOUT = 15 * 60

def die(m):
    print('::error::' + str(m)[:900], flush=True); sys.exit(m)

def main():
    key = os.environ.get('GEMINI_API_KEY') or die('✗ السر GEMINI_API_KEY غير موجود')
    production = os.environ['PRODUCTION'].strip()
    output = os.environ['OUTPUT'].strip()
    prompt = os.environ['PROMPT'].strip()
    tier = os.environ.get('TIER', 'lite').strip()
    duration = int(os.environ.get('DURATION', '4'))
    image = os.environ.get('IMAGE', '').strip()
    aspect = os.environ.get('ASPECT', '9:16').strip()
    max_cost = float(os.environ.get('MAX_COST', '0.5'))

    if not prompt: die('✗ الوصف (prompt) فارغ')
    if tier not in MODELS: die(f'✗ النسخة يجب أن تكون lite أو fast، لا {tier}')
    if duration not in DURATIONS: die(f'✗ المدة يجب أن تكون 4 أو 6 أو 8، لا {duration}')
    if aspect not in ('9:16', '16:9'): die('✗ الإطار يجب أن يكون 9:16 أو 16:9')
    if not output.endswith('.mp4'): output += '.mp4'
    out_path = f'productions/{production}/{output}'
    if os.path.exists(out_path): die(f'✗ الملف موجود: {out_path} (احذفه أو غيّر الاسم)')

    model, rate = MODELS[tier]
    cost = rate * (OMNI_MAX_SECONDS if model.startswith('gemini-omni') else duration)
    print(f'النموذج: {model} · المدة: {duration} ث · 720p · {aspect} · فيديو واحد')
    print(f'التكلفة التقديرية: {cost:.2f}$ (السقف {max_cost:.2f}$)')
    if cost > max_cost: die('✗ التكلفة أعلى من السقف، أُوقف التشغيل قبل أي صرف')

    kw = {}
    if image:
        if not os.path.exists(image): die(f'✗ صورة البداية غير موجودة: {image}')
        mime = mimetypes.guess_type(image)[0] or 'image/png'
        kw['image'] = types.Image(image_bytes=open(image, 'rb').read(), mime_type=mime)
        print(f'صورة البداية: {image}')

    client = genai.Client(api_key=key)
    if model.startswith('gemini-omni'):
        import base64
        if image: die('✗ صورة البداية غير مدعومة بعد في مسار Omni بهذه الأداة')
        it = client.interactions.create(
            model=model,
            input=f'{prompt} The clip is about {duration} seconds long.',
            response_format={'type': 'video', 'aspect_ratio': aspect, 'resolution': '720p'},
        )
        ov = getattr(it, 'output_video', None)
        if not ov or not getattr(ov, 'data', None): die(f'✗ لا فيديو في النتيجة: {str(it)[:600]}')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        data = ov.data
        open(out_path, 'wb').write(base64.b64decode(data) if isinstance(data, str) else data)
        print(f'✓ حُفظ: {out_path} ({os.path.getsize(out_path) // 1024} ك.ب) · السقف التقديري {cost:.2f}$ (التكلفة الفعلية 0.10$ لكل ثانية من المقطع)')
        print(f'::notice title=veo::saved={out_path} model={model} cost_cap≈{cost:.2f}$')
        return
    config = types.GenerateVideosConfig(
        number_of_videos=1,          # إلزامي: مقطع واحد فقط
        duration_seconds=duration,
        resolution='720p',
        aspect_ratio=aspect,
    )
    op = client.models.generate_videos(model=model, prompt=prompt, config=config, **kw)
    start = time.time()
    while not op.done:
        if time.time() - start > TIMEOUT: die('✗ انتهت المهلة (15 دقيقة) دون نتيجة')
        time.sleep(15)
        op = client.operations.get(op)
        print(f'… قيد التوليد ({int(time.time() - start)} ث)')

    if op.error: die(f'✗ فشل التوليد: {op.error}')
    vids = (op.response.generated_videos if op.response else None) or []
    if not vids: die('✗ لا فيديو في النتيجة (قد يكون رُفض لسياسة المحتوى؛ التوليد الفاشل لا يُفوتر)')
    if len(vids) > 1: print(f'! تنبيه: عاد {len(vids)} مقاطع رغم طلب واحد؛ حُفظ الأول فقط')

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    client.files.download(file=vids[0].video)
    vids[0].video.save(out_path)
    print(f'✓ حُفظ: {out_path} ({os.path.getsize(out_path) // 1024} ك.ب) · التكلفة التقديرية {cost:.2f}$')
    print(f'::notice title=veo::saved={out_path} model={model} seconds={duration} cost≈{cost:.2f}$')

if __name__ == '__main__':
    try: main()
    except SystemExit: raise
    except Exception as e: die(f'{type(e).__name__}: {e}')
