// مسار V6 — مختبر الفيديو. يتبع خطوات الحقيبة الخمس نفسها.
const STEPS = ["المهمة", "الجمهور والقيود", "خريطة فيديوك", "البرومبتات", "التحقق"];
const KEY = "masar_v6_state";
const blank = () => ({
  step: 0,
  task: { verb: "", type: "", topic: "", length: "", success: "" },
  aud: { who: "", level: "", where: "", lang: "", action: "" },
  con: { budget: "", time: "", privacy: "", skill: "" },
  pick: "", picks: {}, checks: {}, log: "", other: "", sent: {}
});
let S = load();
function load() { try { return Object.assign(blank(), JSON.parse(localStorage.getItem(KEY)) || {}); } catch (e) { return blank(); } }
function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
const app = document.getElementById("app"), nav = document.getElementById("steps");
const SB = { url: "https://nmbbahzzogspuuvpsxud.supabase.co", key: "sb_publishable_OHbaA9Rse47v5pw_0Juafg_RbeorWMM" };
function sessionId() { try { let v = localStorage.getItem("masar_v6_sid"); if (!v) { v = Math.random().toString(36).slice(2, 12); localStorage.setItem("masar_v6_sid", v); } return v; } catch (e) { return "na"; } }
async function logEvent(ev) {
  const clip = v => (v == null || v === "" ? null : String(v).slice(0, 40));
  const row = { kind: ev.kind, video_type: clip(ev.video_type), tool: clip(ev.tool), budget: clip(S.con.budget), skill: clip(S.con.skill), lang: clip(S.aud.lang), useful: ev.useful || null, note: ev.note ? String(ev.note).slice(0, 500) : null, session: sessionId() };
  try {
    const r = await fetch(SB.url + "/rest/v1/masar_v6_events", { method: "POST", headers: { apikey: SB.key, "Content-Type": "application/json", Prefer: "return=minimal" }, body: JSON.stringify(row) });
    return r.ok;
  } catch (e) { return false; }
}
const esc = s => String(s || "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const OPT = {
  verb: ["إنشاء", "تحرير", "تحويل", "ترجمة"],
  length: ["أقل من دقيقة", "من 1 إلى 3 دقائق", "من 3 إلى 5 دقائق", "أكثر من 5 دقائق"],
  level: ["مبتدئ", "لديه معرفة أساسية", "متخصص"],
  where: ["الهاتف", "الحاسوب", "شاشة قاعة"],
  lang: ["العربية الفصحى", "لهجة محلية", "الإنجليزية", "العربية والإنجليزية"],
  action: ["يفهم", "ينفّذ", "يتخذ قرارًا"],
  budget: ["مجاني فقط", "مبلغ بسيط", "لا مانع من الدفع"],
  time: ["اليوم", "خلال أسبوع", "لا يوجد موعد ضيق"],
  privacy: ["لا توجد بيانات حساسة", "توجد بيانات حساسة"],
  skill: ["مبتدئ في الأدوات", "متوسط", "متمرس"]
};

function chips(group, field, opts) {
  return `<div class="chips" data-g="${group}" data-f="${field}">${opts.map(o =>
    `<button type="button" aria-pressed="${S[group][field] === o}">${esc(o)}</button>`).join("")}</div>`;
}
function text(group, field, ph) {
  return `<input type="text" data-g="${group}" data-f="${field}" value="${esc(S[group][field])}" placeholder="${esc(ph)}">`;
}
function bind() {
  app.querySelectorAll(".chips[data-g]").forEach(c => c.addEventListener("click", e => {
    const b = e.target.closest("button"); if (!b) return;
    S[c.dataset.g][c.dataset.f] = b.textContent; save(); render();
  }));
  app.querySelectorAll("input[type=text][data-g]").forEach(i => i.addEventListener("input", () => {
    S[i.dataset.g][i.dataset.f] = i.value; save(); updateNext();
  }));
  app.querySelectorAll(".types button").forEach(b => b.addEventListener("click", () => {
    S.task.type = b.dataset.t; save(); render();
  }));
  const go = (d) => { S.step = Math.max(0, Math.min(4, S.step + d)); save(); render(); window.scrollTo(0, 0); };
  const n = document.getElementById("next"), p = document.getElementById("prev");
  if (n) n.addEventListener("click", () => {
    const m = S.step < 2 ? missing(S.step) : [];
    if (!m.length) return go(1);
    app.querySelectorAll(".flag").forEach(e => e.classList.remove("flag"));
    m.forEach(([f]) => { const el = f === "type" ? app.querySelector(".types") : app.querySelector(`[data-f="${f}"]`); if (el) el.classList.add("flag"); });
    const first = m[0][0] === "type" ? app.querySelector(".types") : app.querySelector(`[data-f="${m[0][0]}"]`);
    if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
  });
  if (p) p.addEventListener("click", () => go(-1));
  updateNext();
}
function ready(step) {
  const t = S.task, a = S.aud, c = S.con;
  if (step === 0) return t.type !== "other" && t.verb && t.type && t.topic.trim() && t.length;
  if (step === 1) return a.who.trim() && a.level && a.where && a.lang && a.action && c.budget && c.time && c.privacy && c.skill;
  return true;
}
function missing(step) {
  const t = S.task, a = S.aud, c = S.con, m = [];
  if (step === 0) {
    if (!t.type || t.type === "other") m.push(["type", "نوع الفيديو"]);
    if (!t.verb) m.push(["verb", "الفعل المطلوب"]);
    if (!t.topic.trim()) m.push(["topic", "الموضوع"]);
    if (!t.length) m.push(["length", "المدة"]);
  }
  if (step === 1) {
    if (!a.who.trim()) m.push(["who", "من سيستخدم الفيديو"]);
    if (!a.level) m.push(["level", "ماذا يعرف مسبقًا"]);
    if (!a.where) m.push(["where", "أين سيشاهده"]);
    if (!a.lang) m.push(["lang", "اللغة والأسلوب"]);
    if (!a.action) m.push(["action", "الإجراء المطلوب"]);
    if (!c.budget) m.push(["budget", "الميزانية"]);
    if (!c.time) m.push(["time", "موعد التسليم"]);
    if (!c.privacy) m.push(["privacy", "الخصوصية"]);
    if (!c.skill) m.push(["skill", "خبرتك بالأدوات"]);
  }
  return m;
}
function updateNext() {
  const h = document.getElementById("need");
  if (h && S.step < 2) { const m = missing(S.step); h.innerHTML = m.length ? "بقي: " + m.map(x => x[1]).join("، ") : "✓ اكتملت الخانات، اضغط «التالي»"; h.className = m.length ? "hint need" : "hint ok"; }
  const n = document.getElementById("next"); if (!n) return;
  n.classList.toggle("dim", !ready(S.step));
}
function taskSentence() {
  const t = S.task, a = S.aud, c = S.con;
  const typ = VIDEO_TYPES[t.type] ? VIDEO_TYPES[t.type].label : "فيديو";
  return `أريد ${t.verb || "[الفعل]"} فيديو من نوع «${typ}» حول «${t.topic || "[الموضوع]"}»، مدته ${t.length || "[المدة]"}، لجمهور ${a.who || "[الجمهور]"} (${a.level || "[المستوى]"})، يشاهده على ${a.where || "[الجهاز]"}، بـ${a.lang || "[اللغة]"}، مع الالتزام بـ: ${c.budget || "[الميزانية]"}، والتسليم ${c.time || "[الموعد]"}.`;
}

// ---------- محرك الترشيح: المعايير الخمسة موزونة بقيود المستخدم ----------
function weights() {
  const a = S.aud, c = S.con;
  const w = { quality: 2, ease: 2, arabic: 2, cost: 2, privacy: 2 };
  if (c.budget === "مجاني فقط") w.cost = 5; else if (c.budget === "مبلغ بسيط") w.cost = 3; else w.cost = 1;
  if (c.skill === "مبتدئ في الأدوات") w.ease = 4; else if (c.skill === "متمرس") w.ease = 1;
  if (c.time === "اليوم") w.ease += 1;
  if (a.lang && a.lang.includes("العربية") || a.lang === "لهجة محلية") w.arabic = 4;
  if (c.privacy === "توجد بيانات حساسة") w.privacy = 5;
  if (a.where === "شاشة قاعة" || c.budget === "لا مانع من الدفع") w.quality += 1;
  return w;
}
function recommend() {
  const w = weights(), type = S.task.type;
  const pool = TOOLS.filter(t => t.types.includes(type));
  const max = Object.values(w).reduce((s, x) => s + x * 5, 0);
  return pool.map(t => {
    const parts = Object.keys(w).map(k => ({ k, v: w[k] * t.scores[k] }));
    const total = parts.reduce((s, p) => s + p.v, 0);
    const reasons = Object.keys(w).filter(k => t.why[k] && t.scores[k] >= 4).sort((x, y) => w[y] - w[x]).slice(0, 3);
    return { t, pct: Math.round(total / max * 100), reasons, w };
  }).sort((a, b) => b.pct - a.pct).slice(0, 2);
}

// ---------- مولّد البرومبت: العناصر الستة ----------
function buildPrompt(tool) {
  const t = S.task, a = S.aud, c = S.con;
  const typ = VIDEO_TYPES[t.type] ? VIDEO_TYPES[t.type].label : "فيديو";
  const role = { edit: "محرر فيديو محترف", slides: "مصمم محتوى تعليمي مرئي", avatar: "كاتب نصوص لفيديوهات المتحدثين", generate: "مخرج بصري يكتب أوصاف مشاهد دقيقة", translate: "مترجم ومحرر فيديو" }[t.type] || "صانع محتوى مرئي";
  const fmt = a.where === "الهاتف" ? "فيديو عمودي 9:16" : "فيديو أفقي 16:9";
  return [
    ["الدور", `أنت ${role}.`],
    ["المهمة", `${t.verb} فيديو من نوع «${typ}» حول: ${t.topic}.`],
    ["السياق", `الجمهور: ${a.who}، مستواهم ${a.level}، ويشاهدون على ${a.where}. المطلوب منهم بعد المشاهدة أن ${a.action}.`],
    ["القيود", `اللغة: ${a.lang}. المدة: ${t.length}. الميزانية: ${c.budget}. موعد التسليم: ${c.time}.${c.privacy === "توجد بيانات حساسة" ? " لا تستخدم أي أسماء أو بيانات حساسة." : ""}`],
    ["صيغة المُخرَج", `${fmt}، مع نص مكتوب على الشاشة لأهم الأفكار${t.type === "avatar" || t.type === "slides" ? "، ونص التعليق الصوتي كاملًا مقسّمًا إلى مقاطع" : ""}.`],
    ["معيار الجودة", `${t.success ? t.success + "، " : ""}واضح ومختصر ومناسب لمستوى الجمهور، ومعلوماته دقيقة.`]
  ];
}

// ---------- خريطة فيديوك ----------
function rankStage(st) {
  const w = weights(), tools = STAGE_TOOLS[st] || [];
  const max = Object.values(w).reduce((x, y) => x + y * 5, 0);
  return tools.map(t => {
    let total = Object.keys(w).reduce((x, k) => x + w[k] * (t.scores[k] || 3), 0);
    if (t.level === "tested") total += 6;
    if (S.con.budget === "مجاني فقط" && !t.free && t.cost.indexOf("اشتراك") < 0) total -= 14;
    return { t, pct: Math.round(total / max * 100) };
  }).sort((a, b) => b.pct - a.pct);
}
function toolById(st, id) { return (STAGE_TOOLS[st] || []).find(t => t.id === id); }
function pickFor(st) { const r = rankStage(st); if (!S.picks) S.picks = {}; if (!S.picks[st] || !toolById(st, S.picks[st])) S.picks[st] = r.length ? r[0].t.id : ""; return S.picks[st]; }
function stagePrompt(st, tool) {
  const t = S.task, a = S.aud, c = S.con, typ = VIDEO_TYPES[t.type] ? VIDEO_TYPES[t.type].label : "فيديو";
  const fmt = a.where === "الهاتف" ? "عمودي 9:16" : "أفقي 16:9";
  const P = {
    script: `أنت كاتب نصوص فيديو تعليمي. اكتب نص تعليق صوتي لفيديو من نوع «${typ}» مدته ${t.length}، عن: ${t.topic}.\nالجمهور: ${a.who}، مستواهم ${a.level}، ويشاهدون على ${a.where}. اللغة: ${a.lang}.\nابدأ بسؤال أو موقف يعرفه المشاهد، ثم الفكرة في خطوات قصيرة، واختم بدعوة واضحة لأن ${a.action}.\nقسّم النص إلى مقاطع مع توقيت تقريبي بالثواني، واقترح ما يظهر على الشاشة في كل مقطع.\nاكتب نسختين: نسخة مشكولة تشكيلًا كاملًا لأداة الصوت، ونسخة بلا تشكيل للترجمة النصية. تجنّب الاختصارات الإنجليزية.${t.success ? "\nمعيار النجاح: " + t.success + "." : ""}`,
    voice: tool && tool.id === "ownvoice" ? `سجّل النص المشكول بصوتك في مكان هادئ، والهاتف على بعد شبر من فمك.\nسجّل أول جملتين واستمع لهما قبل تسجيل النص كاملًا.` : `في WaveSpeed افتح نموذج ElevenLabs Multilingual V2.\n1. الصق أول جملتين فقط من النص المشكول، وجرّب صوتًا أو صوتين.\n2. استمع للنطق والوقفات (…) ونبرة الأسئلة.\n3. بالصوت الفائز ولّد النص الكامل، وانظر إلى التكلفة قبل الضغط.\n4. قِس المدة الفعلية؛ عليها يُبنى توقيت المشاهد.`,
    avatar: `اقطع من الصوت الكامل مقطع الافتتاح ومقطع الختام فقط (عند الوقفات).\nفي InfiniteTalk: صورة وجه أمامي ${fmt} بدقة 720p على الأقل + مقطع الصوت + 720p.\nابدأ بالمقطع الأقصر، وتأكد أن السعر يطابق مدته قبل الضغط.\nوصف الحركة:\nA friendly professional presenter speaking directly to the camera, natural subtle head movements, calm expression, steady background`,
    slides: `صمّم صورًا بدقة ${a.where === "الهاتف" ? "1080×1920" : "1920×1080"} لفيديو عن: ${t.topic}.\nصورة لكل مقطع من النص، وفي كل صورة جملة واحدة كبيرة تُقرأ في 3 ثوانٍ من الهاتف.\nاستخدم ألوان هويتك وخطًا عربيًا واضحًا، واترك أسفل الصورة فارغًا للترجمة النصية.`,
    generate: `مشهد بصري لفيديو عن: ${t.topic}.\nاكتب لكل مشهد: المكان، والإضاءة، وحركة الكاميرا، والمدة (3–5 ثوانٍ).\nولّد مشهدًا واحدًا أولًا واحكم عليه قبل البقية. لا تطلب نصوصًا مكتوبة داخل المشهد؛ أضفها في المونتاج.`,
    recording: `قبل التصوير: إضاءة من الأمام، وخلفية هادئة، والهاتف ${fmt} على حامل.\nصوّر لقطة تجريبية من 10 ثوانٍ واسمعها.\nاقرأ النص بلا تشكيل من شاشة أمامك، ومقطعًا مقطعًا.`,
    translate: `ترجم النص التالي إلى ${a.lang} لفيديو موجّه إلى ${a.who}.\nحافظ على المعنى لا الحرف، وبجمل قصيرة تصلح للترجمة النصية.\nأعطني نسختين: نصًا مقسّمًا للترجمة النصية بتوقيت تقريبي، ونسخة متصلة للدبلجة.`,
    montage: tool && tool.id === "capcut-m" ? `في CapCut: ضع الصوت الكامل أولًا، ثم المشاهد فوقه بحسب التوقيت.\nأضف ترجمة نصية تلقائية وراجعها كلمة كلمة، ووحّد مستوى الصوت، ثم صدّر ${fmt} بدقة 1080p.` : `اجمع هذه الملفات في فيديو ${fmt} بدقة 1080p: [ارفع الصوت الكامل، ومقاطع الأفاتار أو التصوير، والصور].\nضع كل صورة على مقطعها من النص، بحركة تقريب بطيئة وانتقال ناعم.\nأضف ترجمة نصية عربية بجمل قصيرة متزامنة مع الكلام أسفل الشاشة، ووحّد مستوى الصوت قرب -16.\nأرسل لي الفيديو لأشاهده على الهاتف قبل الاعتماد.`
  };
  return P[st] || "";
}

// ---------- الشاشات ----------
const screens = [
  () => `<details class="intro" ${S.task.type ? "" : "open"}><summary>شاهد: كيف تعمل منصة مسار (دقيقة واحدة)</summary><video controls preload="metadata" playsinline src="media/masar-explainer-v1.mp4"></video></details>
  <h1>ما المهمة التي تريد إنجازها؟</h1>
  <p class="lead">قبل أن تسأل «ما الأداة؟» اسأل: ماذا أريد بالضبط؟</p>
  <div class="card"><h3>نوع الفيديو</h3><div class="types">${Object.entries(VIDEO_TYPES).map(([k, v]) =>
    `<button type="button" data-t="${k}" aria-pressed="${S.task.type === k}"><b>${v.label}</b><span>${v.hint}</span></button>`).join("")}
    <button type="button" data-t="other" aria-pressed="${S.task.type === "other"}"><b>نوع آخر</b><span>لم أجد ما أحتاجه في القائمة</span></button></div>
    ${S.task.type === "other" ? `<label class="f">ما الذي تحتاجه؟ <small>لا تكتب أسماء أو بيانات شخصية</small></label><textarea id="other" maxlength="500" placeholder="مثال: فيديو بلغة الإشارة، أو بث مباشر…">${esc(S.other)}</textarea>
    <div class="actions"><button type="button" class="btn pri" id="sendReq">أرسل الطلب</button><span class="hint" id="reqMsg">${S.sent.request ? "سُجّل طلبك. شكرًا لك." : ""}</span></div>` : ""}</div>
  <div class="card"><h3>العناصر الأربعة</h3>
    <label class="f">1. الفعل المطلوب</label>${chips("task", "verb", OPT.verb)}
    <label class="f">2. الموضوع <small>عمّ يتحدث الفيديو؟</small></label>${text("task", "topic", "مثال: الاستخدام المسؤول للذكاء الاصطناعي في البحث العلمي")}
    <label class="f">3. المُخرَج: المدة</label>${chips("task", "length", OPT.length)}
    <label class="f">4. معيار النجاح <small>اختياري</small></label>${text("task", "success", "مثال: يفهمه المبتدئ من المشاهدة الأولى")}
  </div>`,
  () => `<h1>لمن؟ وضمن أي قيود؟</h1>
  <p class="lead">الجمهور والقيود ليست تفاصيل إضافية، بل معايير الاختيار نفسها.</p>
  <div class="card"><h3>الجمهور</h3>
    <label class="f">من سيستخدم الفيديو؟</label>${text("aud", "who", "مثال: موظفون جدد، طلاب جامعة، باحثون")}
    <label class="f">ماذا يعرف مسبقًا؟</label>${chips("aud", "level", OPT.level)}
    <label class="f">أين سيشاهده؟</label>${chips("aud", "where", OPT.where)}
    <label class="f">اللغة والأسلوب</label>${chips("aud", "lang", OPT.lang)}
    <label class="f">ما الإجراء المطلوب منه بعد المشاهدة؟</label>${chips("aud", "action", OPT.action)}
  </div>
  <div class="card"><h3>القيود</h3>
    <label class="f">الميزانية</label>${chips("con", "budget", OPT.budget)}
    <label class="f">موعد التسليم</label>${chips("con", "time", OPT.time)}
    <label class="f">الخصوصية</label>${chips("con", "privacy", OPT.privacy)}
    <label class="f">خبرتك بأدوات الفيديو</label>${chips("con", "skill", OPT.skill)}
  </div>
  <div class="sentence"><b>مهمتك في جملة واحدة:</b><br>${esc(taskSentence())}</div>`,
  () => {
    const stages = PIPELINES[S.task.type] || [];
    if (!stages.length) return `<h1>خريطة فيديوك</h1><div class="empty">لا توجد خريطة لهذا النوع بعد.</div>`;
    return `<h1>خريطة فيديوك</h1>
    <p class="lead">فيديو «${esc(VIDEO_TYPES[S.task.type].label)}» يمر بـ${stages.length} مراحل. في كل مرحلة: أداة مرشحة، وبديل، ودرس من تجربة حقيقية.</p>
    ${stages.map((st, i) => {
      const def = STAGE_DEFS[st], ranked = rankStage(st), cur = pickFor(st);
      return `<div class="stage"><div class="shd"><span class="snum">${i + 1}</span><h2>${def.icon} ${def.name}</h2></div>
      <div class="opts">${ranked.slice(0, 2).map((r, j) => `<button type="button" class="opt2 ${cur === r.t.id ? "on" : ""}" data-stage="${st}" data-tool="${r.t.id}">
        <span class="rk">${j === 0 ? "الترشيح" : "البديل"}</span><b>${esc(r.t.name)}</b>
        <span class="ver ${r.t.level}">${r.t.level === "tested" ? "مختبرة فعليًا" : "مراجعة من التوثيق"}</span>
        <span class="cost">${esc(r.t.cost)}</span><span class="nt">${esc(r.t.note)}</span></button>`).join("")}</div>
      <div class="lesson"><b>درس من التجربة:</b> ${esc(def.lesson)}</div></div>`;
    }).join("")}
    <p class="hint">«مختبرة فعليًا» = استُخدمت في صنع فيديو حقيقي. «مراجعة» = من توثيق الأداة فقط.</p>`;
  },
  () => {
    const stages = PIPELINES[S.task.type] || [];
    return `<h1>برومبتات جاهزة لكل مرحلة</h1>
    <p class="lead">انسخ برومبت كل مرحلة والصقه في أداتها، بالترتيب.</p>
    ${stages.map((st, i) => {
      const tool = toolById(st, pickFor(st)), p = stagePrompt(st, tool);
      return `<div class="stage"><div class="shd"><span class="snum">${i + 1}</span><h2>${STAGE_DEFS[st].icon} ${STAGE_DEFS[st].name} <small>· ${esc(tool ? tool.name : "")}</small></h2></div>
      <div class="prompt">${esc(p)}</div>
      <div class="actions"><button type="button" class="btn sec" data-copy="${i}">نسخ</button><span class="hint" id="cp${i}"></span></div>
      <textarea id="pt${i}" hidden>${esc(p)}</textarea></div>`;
    }).join("")}`;
  },
  () => {
    const stages = PIPELINES[S.task.type] || [];
    const items = ["هل تحقق الهدف؟", "هل المعلومات دقيقة؟", "هل يعمل الملف بصورة صحيحة؟", "هل النص واضح؟", "هل الروابط صحيحة؟", "هل حميت البيانات الحساسة؟", "هل يناسب المُخرَج الجمهور والجهاز؟"];
    const all = items.every((_, i) => S.checks[i]);
    return `<h1>نفّذ نسخة صغيرة… ثم تحقق</h1>
    <p class="lead">لا تعتمد أول نتيجة. شاهد الفيديو على الهاتف، ثم افحصه بهذه القائمة.</p>
    <div class="card checks no-print"><h3>قائمة التحقق النهائية</h3>${items.map((t, i) =>
      `<label><input type="checkbox" data-c="${i}" ${S.checks[i] ? "checked" : ""}><span>${t}</span></label>`).join("")}
      <p class="hint">${all ? "كل الإجابات «نعم»: يمكنك اعتماد النتيجة." : "إذا كانت إجابة أي سؤال «لا»، فعدّل التعليمات وأعد التنفيذ الصغير."}</p></div>
    <div class="summary"><h3 style="margin:0;color:var(--gold)">بطاقة القرار</h3><dl>
      <dt>المهمة</dt><dd>${esc(taskSentence())}</dd>
      <dt>خريطة الفيديو</dt><dd>${stages.map((st, i) => `${i + 1}. ${STAGE_DEFS[st].name}: <b>${esc((toolById(st, pickFor(st)) || {}).name || "")}</b>`).join("<br>")}</dd>
      <dt>طريقة التحقق</dt><dd>${all ? "اجتازت النتيجة قائمة التحقق كاملة." : "قيد التحقق."}</dd></dl></div>
    <div class="card no-print" style="margin-top:14px"><h3>هل كانت الخريطة مفيدة لك؟</h3>
      ${S.sent.feedback ? `<p class="hint">شكرًا لك، سُجّل رأيك.</p>` : `<div class="chips" id="useful">${[["yes","نعم"],["partly","جزئيًا"],["no","لا"]].map(([v,l]) => `<button type="button" data-u="${v}" aria-pressed="${S.useful === v}">${l}</button>`).join("")}</div>
      <label class="f">ملاحظة <small>اختيارية · لا تكتب بيانات شخصية</small></label><textarea id="fbNote" maxlength="500"></textarea>
      <div class="actions"><button type="button" class="btn sec" id="sendFb" ${S.useful ? "" : "disabled"}>أرسل رأيك</button><span class="hint" id="fbMsg"></span></div>`}</div>
    <div class="actions"><button type="button" class="btn pri" onclick="window.print()">حفظ بطاقة القرار PDF</button>
    <button type="button" class="btn sec" id="reset">مهمة جديدة</button></div>`;
  }
];

function render() {
  nav.innerHTML = STEPS.map((s, i) => `<button type="button" class="${i < S.step ? "done" : i === S.step ? "cur" : ""}" ${i <= S.step ? "" : "disabled title=\"أكمل الخطوة الحالية أولًا\""} data-s="${i}"><span class="dot"></span>${i + 1}. ${s}</button>`).join("");
  nav.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { S.step = +b.dataset.s; save(); render(); }));
  app.innerHTML = screens[S.step]() + (S.step < 4 ? `<div class="actions">
    ${S.step > 0 ? `<button type="button" class="btn sec" id="prev">→ السابق</button>` : ""}
    <button type="button" class="btn pri" id="next">التالي ←</button>
    ${S.step < 2 ? `<span class="hint need" id="need"></span>` : ""}</div>` :
    `<div class="actions no-print"><button type="button" class="btn sec" id="prev">→ السابق</button></div>`);
  bind();
  app.querySelectorAll("[data-stage]").forEach(b => b.addEventListener("click", () => { S.picks[b.dataset.stage] = b.dataset.tool; save(); render(); }));
  app.querySelectorAll("[data-copy]").forEach(b => b.addEventListener("click", async () => {
    const i = b.dataset.copy, v = document.getElementById("pt" + i).value;
    try { await navigator.clipboard.writeText(v); } catch (e) { const t = document.createElement("textarea"); t.value = v; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); }
    document.getElementById("cp" + i).textContent = "تم النسخ";
  }));
  app.querySelectorAll("[data-pick]").forEach(b => b.addEventListener("click", () => { S.pick = b.dataset.pick; save(); render(); }));
  app.querySelectorAll("[data-c]").forEach(c => c.addEventListener("change", () => { S.checks[c.dataset.c] = c.checked; save(); render(); }));
  const cp = document.getElementById("copy");
  if (cp) cp.addEventListener("click", async () => {
    const v = document.getElementById("plain").value;
    try { await navigator.clipboard.writeText(v); } catch (e) { const t = document.createElement("textarea"); t.value = v; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); }
    document.getElementById("copied").textContent = "تم النسخ";
  });
  const ot = document.getElementById("other");
  if (ot) ot.addEventListener("input", () => { S.other = ot.value; save(); });
  const sr = document.getElementById("sendReq");
  if (sr) sr.addEventListener("click", async () => {
    if (!S.other.trim()) { document.getElementById("reqMsg").textContent = "اكتب ما تحتاجه أولًا."; return; }
    sr.disabled = true; document.getElementById("reqMsg").textContent = "جارٍ الإرسال…";
    const ok = await logEvent({ kind: "request", video_type: "other", note: S.other });
    if (ok) { S.sent.request = true; save(); document.getElementById("reqMsg").textContent = "سُجّل طلبك. شكرًا لك."; }
    else { sr.disabled = false; document.getElementById("reqMsg").textContent = "تعذّر الإرسال الآن. حاول لاحقًا."; }
  });
  app.querySelectorAll("[data-u]").forEach(b => b.addEventListener("click", () => { S.useful = b.dataset.u; save(); render(); }));
  const sf = document.getElementById("sendFb");
  if (sf) sf.addEventListener("click", async () => {
    sf.disabled = true; document.getElementById("fbMsg").textContent = "جارٍ الإرسال…";
    const ok = await logEvent({ kind: "feedback", video_type: S.task.type, tool: (PIPELINES[S.task.type] || []).map(st => pickFor(st)).join(","), useful: S.useful, note: document.getElementById("fbNote").value });
    if (ok) { S.sent.feedback = true; save(); render(); }
    else { sf.disabled = false; document.getElementById("fbMsg").textContent = "تعذّر الإرسال الآن. حاول لاحقًا."; }
  });
  if (S.step === 4) {
    const sig = (PIPELINES[S.task.type] || []).map(st => pickFor(st)).join(",");
    if (S.sent.decision !== sig) { S.sent.decision = sig; save(); logEvent({ kind: "decision", video_type: S.task.type, tool: sig, note: sig }); }
  }
  const rs = document.getElementById("reset");
  if (rs) rs.addEventListener("click", () => { S = blank(); save(); render(); window.scrollTo(0, 0); });
}
render();
