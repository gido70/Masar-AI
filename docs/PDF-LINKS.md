# روابط ملفات PDF المنفصلة (مستودع lib-6931de، 14 أكتوبر 2026)

> مستودع منفصل بلا صفحة رئيسية: حذف اسم الملف من الرابط يعطي 404. **أي تحديث لملف في resources/ يجب نسخه هنا بالاسم نفسه** (حتى تبقى روابط CPS صحيحة).

| الملف الأصلي في المنصة | الرابط المنفصل |
|---|---|
| resources/masar-unit-1.pdf | https://gido70.github.io/lib-6931de/70b6329b6710.pdf |
| resources/masar-unit-2.pdf | https://gido70.github.io/lib-6931de/682c19a6f43b.pdf |
| resources/masar-unit-3.pdf | https://gido70.github.io/lib-6931de/d01378247d8a.pdf |
| resources/masar-unit-4.pdf | https://gido70.github.io/lib-6931de/12698bc9da54.pdf |
| resources/masar-unit-5.pdf | https://gido70.github.io/lib-6931de/e1c236f485f5.pdf |
| resources/masar-workbook.pdf | https://gido70.github.io/lib-6931de/25cead20b5a0.pdf |
| resources/video/video-unit-1.pdf | https://gido70.github.io/lib-6931de/408dfa6753be.pdf |
| resources/video/video-unit-2.pdf | https://gido70.github.io/lib-6931de/4ac884106872.pdf |
| resources/video/video-unit-3.pdf | https://gido70.github.io/lib-6931de/b0e4c08102a8.pdf |
| resources/video/video-unit-4.pdf | https://gido70.github.io/lib-6931de/5b8f266f68b8.pdf |
| resources/video/video-unit-5.pdf | https://gido70.github.io/lib-6931de/e38155ff9266.pdf |
| resources/video/video-unit-6.pdf | https://gido70.github.io/lib-6931de/269b68efa6df.pdf |
| resources/free-workbook-solved.pdf | https://gido70.github.io/lib-6931de/2866e01294f1.pdf |
| resources/video-workbook-solved.pdf | https://gido70.github.io/lib-6931de/5f77edb3c02e.pdf |

> **استثناء مقصود (17 أكتوبر 2026):** نسخة CPS من الكراسة المجانية (25cead20b5a0.pdf) فيها زر «افتح النموذج المحلول» في الصفحة الأولى، لأن CPS لا يقبل ملفًا ثانيًا ولا يجعل روابط النص قابلة للضغط. أما نسختا منصة مسار في resources/ فتبقيان بلا الزر (فيها الكراسة التفاعلية والنموذج المحلول منفصلين). لإعادة صنع نسخة CPS: tools/add_solved_button.py.
| resources/cps/video-workbook-cps.pdf (كراسة أوراق العمل لحقيبة الفيديو، نسخة CPS بزر النموذج المحلول) | https://gido70.github.io/lib-6931de/d294230d4d78.pdf |
> **نسخ CPS الخاصة** محفوظة في resources/cps/ (الكراستان بزر النموذج المحلول)، وتظهر في الورشة ← ملف كل حقيبة ← «نسخة منصة CPS». منصة مسار نفسها تعمل بطريقتها (المشغّل، والكراسة التفاعلية، والنموذج المحلول المنفصل) ولا تتغير لأجل CPS.

> **إضافة (29 أكتوبر 2026):** نسختا CPS (25cead20b5a0.pdf وd294230d4d78.pdf) أُضيفت في آخر كل منهما صفحة «الكراسة التفاعلية بالأمثلة» بزر إلى p/free-workbook.html وp/video-workbook.html. الصفحات القائمة لم تتغير، والرابط نفسه، فلا عنصر جديد في CPS ولا تغيير في الدرجات. لإعادة الصنع: tools/add_workbook_page.py.

> **تصحيح (29 أكتوبر 2026، بطلب دردشة CPS):** زر الصفحة الأخيرة في نسختي CPS صار يفتح نسخة مستقلة من الكراسة على lib-6931de بلا أي ارتباط بموقع مسار: f5a3c0471cfe.html (الذكاء الاصطناعي) و9a886deed728.html (الفيديو)، وحُذف الرابط المطبوع تحت الزر. المصدر: resources/cps/web/، والصنع: tools/build_standalone_workbook.py ثم tools/add_workbook_page.py من النسخة الأصلية للكراسة.
