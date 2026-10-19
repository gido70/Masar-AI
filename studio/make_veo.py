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
    'fast': ('veo-3.1-fast-generate-preview', 0.10),
}
DURATIONS = (4, 6, 8)
TIMEOUT = 15 * 60

def main():
    key = os.environ.get('GEMINI_API_KEY') or sys.exit('✗ السر GEMINI_API_KEY غير موجود')
    production = os.environ['PRODUCTION'].strip()
    output = os.environ['OUTPUT'].strip()
    prompt = os.environ['PROMPT'].strip()
    tier = os.environ.get('TIER', 'lite').strip()
    duration = int(os.environ.get('DURATION', '4'))
    image = os.environ.get('IMAGE', '').strip()
    aspect = os.environ.get('ASPECT', '9:16').strip()
    max_cost = float(os.environ.get('MAX_COST', '0.5'))

    if not prompt: sys.exit('✗ الوصف (prompt) فارغ')
    if tier not in MODELS: sys.exit(f'✗ النسخة يجب أن تكون lite أو fast، لا {tier}')
    if duration not in DURATIONS: sys.exit(f'✗ المدة يجب أن تكون 4 أو 6 أو 8، لا {duration}')
    if aspect not in ('9:16', '16:9'): sys.exit('✗ الإطار يجب أن يكون 9:16 أو 16:9')
    if not output.endswith('.mp4'): output += '.mp4'
    out_path = f'productions/{production}/{output}'
    if os.path.exists(out_path): sys.exit(f'✗ الملف موجود: {out_path} (احذفه أو غيّر الاسم)')

    model, rate = MODELS[tier]
    cost = rate * duration
    print(f'النموذج: {model} · المدة: {duration} ث · 720p · {aspect} · فيديو واحد')
    print(f'التكلفة التقديرية: {cost:.2f}$ (السقف {max_cost:.2f}$)')
    if cost > max_cost: sys.exit('✗ التكلفة أعلى من السقف، أُوقف التشغيل قبل أي صرف')

    kw = {}
    if image:
        if not os.path.exists(image): sys.exit(f'✗ صورة البداية غير موجودة: {image}')
        mime = mimetypes.guess_type(image)[0] or 'image/png'
        kw['image'] = types.Image(image_bytes=open(image, 'rb').read(), mime_type=mime)
        print(f'صورة البداية: {image}')

    client = genai.Client(api_key=key)
    config = types.GenerateVideosConfig(
        number_of_videos=1,          # إلزامي: مقطع واحد فقط
        duration_seconds=duration,
        resolution='720p',
        aspect_ratio=aspect,
    )
    op = client.models.generate_videos(model=model, prompt=prompt, config=config, **kw)
    start = time.time()
    while not op.done:
        if time.time() - start > TIMEOUT: sys.exit('✗ انتهت المهلة (15 دقيقة) دون نتيجة')
        time.sleep(15)
        op = client.operations.get(op)
        print(f'… قيد التوليد ({int(time.time() - start)} ث)')

    if op.error: sys.exit(f'✗ فشل التوليد: {op.error}')
    vids = (op.response.generated_videos if op.response else None) or []
    if not vids: sys.exit('✗ لا فيديو في النتيجة (قد يكون رُفض لسياسة المحتوى؛ التوليد الفاشل لا يُفوتر)')
    if len(vids) > 1: print(f'! تنبيه: عاد {len(vids)} مقاطع رغم طلب واحد؛ حُفظ الأول فقط')

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    client.files.download(file=vids[0].video)
    vids[0].video.save(out_path)
    print(f'✓ حُفظ: {out_path} ({os.path.getsize(out_path) // 1024} ك.ب) · التكلفة التقديرية {cost:.2f}$')
    print(f'::notice title=veo::saved={out_path} model={model} seconds={duration} cost≈{cost:.2f}$')

if __name__ == '__main__':
    main()
