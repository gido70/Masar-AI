-- Align trainer-portal records with the approved Masar AI worksheet through step 12.
-- Safe to re-run: every row is upserted by its fixed step number.

insert into public.masar_steps
  (step_no, title, status, output_summary, evidence_status)
values
  (1,  'مجال المعرفة والفكرة',              'completed', 'صياغة مجال المشكلة والمخرج',                                      'documented'),
  (2,  'العميل الأساسي',                     'completed', 'تحديد مستخدم عربي له مهمة وقيود',                                'documented'),
  (3,  'رحلة العميل الكاملة',                'completed', 'خريطة قبل وأثناء وبعد ثلاثة أشهر',                              'documented'),
  (4,  'تقدير السوق المتاح',                 'completed', 'تقدير صادق قيد الحصر واختبار الاستجابة والدفع والسعر',          'documented'),
  (5,  'الاحتياجات الرئيسية',                'completed', 'اختيار دون تشتت، وترشيح موثوق، وبداية عملية',                  'documented'),
  (6,  'القيمة الفريدة والمنهجية',           'completed', 'قرار مفسر لا موسوعة أدوات',                                  'documented'),
  (7,  'اختيار صيغة المنتج',                 'completed', 'منصة رقمية تفاعلية ذاتية الاستخدام',                           'documented'),
  (8,  'رحلة التعلم والتحول',                'completed', 'تحول قابل للقياس يبدأ بقرار مفسر وخطوة تنفيذ',                 'documented'),
  (9,  'مخطط المحتوى الأولي',                'completed', 'ست وحدات؛ لكل وحدة نتيجة واحدة ومستوى بلوم ووسيلة تحقق',       'documented'),
  (10, 'تحديد نموذج التوزيع',                'completed', 'قنوات مباشرة موثوقة وقناة نمو تُختبر تدريجيًا',                'documented'),
  (11, 'تصميم قمع التسويق',                  'completed', 'وعي بالمشكلة ثم تجربة المنهجية ثم قرار الانضمام المبكر',       'documented'),
  (12, 'صفحة الهبوط والعرض التسويقي',        'completed', 'وعد قصير ودليل صادق ودعوة إلى المسار التجريبي',               'documented')
on conflict (step_no) do update
set title = excluded.title,
    status = excluded.status,
    output_summary = excluded.output_summary,
    evidence_status = excluded.evidence_status,
    updated_at = timezone('utc', now());

insert into public.masar_evidence
  (step_no, title, description, evidence_type, verification_status)
select
  12,
  'ملف أوراق عمل مسار AI — الخطوات 1–12',
  'المرجع المعتمد لمواءمة الإندكس والمنصة وبوابة المدرب حتى الخطوة 12.',
  'document',
  'documented'
where not exists (
  select 1
  from public.masar_evidence
  where step_no = 12
    and title = 'ملف أوراق عمل مسار AI — الخطوات 1–12'
);
