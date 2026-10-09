// «خريطة فيديوك» — مراحل الفيديو حسب نوعه، وأدوات كل مرحلة، والدروس من تجربة حقيقية (أكتوبر 2026).
// level: "tested" جُرِّبت فعليًا في تجربة فيديو شرح منصة مسار | "reviewed" مراجعة من التوثيق فقط.

const STAGE_DEFS = {
  script:    { name: "النص", icon: "✍️", lesson: "شكّل النص تشكيلًا كاملًا قبل تحويله إلى صوت، واستخدم الأسماء العربية بدل الاختصارات الإنجليزية مثل «AI». اقرأه بصوت عالٍ مرة واحدة قبل الانتقال." },
  voice:     { name: "الصوت", icon: "🎙️", lesson: "جرّب جملتين أولًا قبل النص الكامل. وتوقّع أن تكون المدة أقصر من تقديرك: نص قدّرناه بـ70 ثانية خرج في 50." },
  avatar:    { name: "الأفاتار", icon: "🧑‍💼", lesson: "اقطع الصوت واجعل الأفاتار في البداية والنهاية فقط. استخدم صورة وجه أمامي واضحة بلا أيدٍ أمام الجسم. وتأكد قبل الضغط أن السعر محسوب على ملفك الفعلي، فهو يُحسب بالثانية." },
  slides:    { name: "الشرائح والصور", icon: "🖼️", lesson: "النص على الشاشة يجب أن يُقرأ في 3 ثوانٍ من الهاتف: جملة واحدة كبيرة لكل صورة. لقطات الشاشة الكاملة تظهر صغيرة جدًا في الفيديو." },
  generate:  { name: "اللقطات المولّدة", icon: "🎬", lesson: "ولّد لقطة واحدة قصيرة واحكم عليها قبل توليد كل المشاهد؛ فالرصيد ينفد بسرعة." },
  recording: { name: "التصوير", icon: "📱", lesson: "إضاءة أمامية، وخلفية هادئة، وصوت قريب من الفم. صوّر لقطة تجريبية من 10 ثوانٍ واسمعها قبل التصوير الكامل." },
  translate: { name: "الترجمة", icon: "🌐", lesson: "ترجم النص المكتوب أولًا وراجعه، ثم حوّله إلى ترجمة نصية أو دبلجة؛ الخطأ في النص يتضاعف في الصوت." },
  montage:   { name: "المونتاج", icon: "🎞️", lesson: "ترجمة نصية بجمل قصيرة متزامنة مع الكلام، ومستوى صوت موحد قرب -16. شاهد النتيجة على الهاتف قبل النشر." }
};

const PIPELINES = {
  avatar:    ["script", "voice", "avatar", "slides", "montage"],
  slides:    ["script", "voice", "slides", "montage"],
  edit:      ["script", "recording", "montage"],
  generate:  ["script", "voice", "generate", "montage"],
  translate: ["translate", "voice", "montage"]
};

const STAGE_TOOLS = {
  script: [
    { id: "claude", name: "Claude", url: "https://claude.ai/", level: "tested", cost: "ضمن اشتراكك", scores: { quality: 5, ease: 5, arabic: 5, cost: 4, privacy: 4 }, note: "كتب نص فيديو شرح مسار مشكولًا ومقسّمًا بالثواني." },
    { id: "chatgpt", name: "ChatGPT", url: "https://chatgpt.com/", level: "reviewed", cost: "نسخة مجانية متاحة", scores: { quality: 4, ease: 5, arabic: 4, cost: 5, privacy: 3 }, note: "بديل شائع لكتابة النصوص." }
  ],
  voice: [
    { id: "elevenlabs", name: "ElevenLabs Multilingual V2 (على WaveSpeed)", url: "https://wavespeed.ai/", level: "tested", cost: "بضعة سنتات لنص دقيقة", scores: { quality: 5, ease: 4, arabic: 5, cost: 4, privacy: 3 }, note: "احترم التشكيل والوقفات (…) في التجربة." },
    { id: "ownvoice", name: "صوتك أنت (تسجيل بالهاتف)", url: "", level: "reviewed", cost: "مجاني", scores: { quality: 3, ease: 4, arabic: 5, cost: 5, privacy: 5 }, note: "مجاني وشخصي، ويحتاج مكانًا هادئًا." }
  ],
  avatar: [
    { id: "infinitetalk", name: "InfiniteTalk (على WaveSpeed)", url: "https://wavespeed.ai/", level: "tested", cost: "≈ 0.06 دولار للثانية بجودة 720p (18 ثانية = 1.14 دولار)", scores: { quality: 5, ease: 4, arabic: 4, cost: 3, privacy: 3 }, note: "وجه ثابت وخلفية ثابتة في المقطعين." },
    { id: "heygen", name: "HeyGen", url: "https://www.heygen.com/", level: "reviewed", cost: "خطة مجانية محدودة بعلامة مائية", scores: { quality: 5, ease: 4, arabic: 4, cost: 2, privacy: 3 }, note: "متحدثون جاهزون ودبلجة." }
  ],
  slides: [
    { id: "claude-design", name: "Claude (تصميم الصور)", url: "https://claude.ai/", level: "tested", cost: "ضمن اشتراكك", scores: { quality: 4, ease: 5, arabic: 5, cost: 4, privacy: 4 }, note: "صمّم صور الفيديو السبع بهوية مسار وخط كبير." },
    { id: "canva", name: "Canva", url: "https://www.canva.com/", level: "reviewed", cost: "نسخة مجانية واسعة", scores: { quality: 4, ease: 5, arabic: 4, cost: 4, privacy: 3 }, note: "قوالب جاهزة كثيرة." }
  ],
  generate: [
    { id: "runway", name: "Runway", url: "https://runwayml.com/", level: "reviewed", cost: "بالرصيد، وقد ينفد بسرعة", scores: { quality: 5, ease: 3, arabic: 2, cost: 2, privacy: 3 }, note: "تحكم بصري عالٍ؛ واجهته إنجليزية." },
    { id: "davinci", name: "DaVinci AI", url: "https://davinci.ai/", level: "reviewed", cost: "خطة مجانية للتجربة", scores: { quality: 4, ease: 4, arabic: 2, cost: 3, privacy: 3 }, note: "يجمع نماذج صور وفيديو متعددة في واجهة واحدة." }
  ],
  recording: [
    { id: "phone", name: "كاميرا الهاتف", url: "", level: "reviewed", cost: "مجاني", scores: { quality: 3, ease: 5, arabic: 5, cost: 5, privacy: 5 }, note: "كافية لفيديو تعليمي مع إضاءة جيدة." }
  ],
  translate: [
    { id: "claude-tr", name: "Claude (ترجمة النص)", url: "https://claude.ai/", level: "reviewed", cost: "ضمن اشتراكك", scores: { quality: 5, ease: 5, arabic: 5, cost: 4, privacy: 4 }, note: "ترجمة النص ومراجعته قبل الصوت." },
    { id: "heygen-tr", name: "HeyGen (دبلجة)", url: "https://www.heygen.com/", level: "reviewed", cost: "مدفوع غالبًا", scores: { quality: 5, ease: 4, arabic: 4, cost: 2, privacy: 3 }, note: "دبلجة مع مزامنة الشفاه." }
  ],
  montage: [
    { id: "claude-studio", name: "Claude (استوديو المونتاج)", url: "https://claude.ai/", level: "tested", cost: "ضمن اشتراكك", scores: { quality: 4, ease: 5, arabic: 5, cost: 4, privacy: 4 }, note: "جمع فيديو شرح مسار مع ترجمة نصية عربية متزامنة، بالمحادثة." },
    { id: "capcut-m", name: "CapCut", url: "https://www.capcut.com/", level: "reviewed", cost: "نسخة مجانية", scores: { quality: 4, ease: 4, arabic: 4, cost: 5, privacy: 2 }, note: "خط زمني يدوي وموسيقى مجانية." }
  ]
};
