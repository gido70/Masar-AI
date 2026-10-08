// مسار V6 — مختبر الفيديو. يتبع خطوات الحقيبة الخمس نفسها.
const STEPS = ["المهمة", "الجمهور والقيود", "الترشيح", "البرومبت", "التحقق"];
const KEY = "masar_v6_state";
const blank = () => ({
  step: 0,
  task: { verb: "", type: "", topic: "", length: "", success: "" },
  aud: { who: "", level: "", where: "", lang: "", action: "" },
  con: { budget: "", time: "", privacy: "", skill: "" },
  pick: "", checks: {}, log: ""
});
let S = load();
function load() { try { return Object.assign(blank(), JSON.parse(localStorage.getItem(KEY)) || {}); } catch (e) { return blank(); } }
function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }
const app = document.getElementById("app"), nav = document.getElementById("steps");
const esc = s => String(s || "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

const OPT = {
  verb: ["إنشاء", "تحرير", "تحويل", "ترجمة"],
  length: ["أقل من دقيقة", "1–3 دقائق", "3–5 دقائق", "أكثر من 5 دقائق"],
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
  app.querySelectorAll(".chips").forEach(c => c.addEventListener("click", e => {
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
  if (n) n.addEventListener("click", () => go(1));
  if (p) p.addEventListener("click", () => go(-1));
  updateNext();
}
function ready(step) {
  const t = S.task, a = S.aud, c = S.con;
  if (step === 0) return t.verb && t.type && t.topic.trim() && t.length;
  if (step === 1) return a.who.trim() && a.level && a.where && a.lang && a.action && c.budget && c.time && c.privacy && c.skill;
  return true;
}
function updateNext() {
  const n = document.getElementById("next"); if (!n) return;
  n.disabled = !ready(S.step);
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

// ---------- الشاشات ----------
const screens = [
  () => `<h1>ما المهمة التي تريد إنجازها؟</h1>
  <p class="lead">قبل أن تسأل «ما الأداة؟» اسأل: ماذا أريد بالضبط؟</p>
  <div class="card"><h3>نوع الفيديو</h3><div class="types">${Object.entries(VIDEO_TYPES).map(([k, v]) =>
    `<button type="button" data-t="${k}" aria-pressed="${S.task.type === k}"><b>${v.label}</b><span>${v.hint}</span></button>`).join("")}</div></div>
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
    const recs = recommend();
    if (!recs.length) return `<h1>الترشيح</h1><div class="empty">لا توجد أداة في الكتالوج الحالي لهذا النوع من الفيديو بعد.</div>`;
    if (!S.pick || !recs.find(r => r.t.id === S.pick)) { S.pick = recs[0].t.id; save(); }
    return `<h1>أداتان مناسبتان لمهمتك</h1>
    <p class="lead">قارنّا الأدوات بالمعايير الخمسة، ووزنّاها بحسب قيودك. اختر واحدة.</p>
    ${recs.map((r, i) => `<div class="rec ${i === 0 ? "top" : ""}">
      <div class="hd"><span class="rank">${i === 0 ? "الترشيح الأول" : "البديل"}</span><h2>${esc(r.t.name)}</h2>
      <span class="ver ${r.t.verify.level}">${{ tested: "مختبرة فعليًا", reviewed: "مراجعة من التوثيق", unverified: "غير متحقق منها" }[r.t.verify.level]}</span>
      <span class="hint">توافق ${r.pct}٪</span></div>
      <div class="bars">${Object.keys(CRITERIA).map(k => `<span>${CRITERIA[k]}</span><span class="bar ${r.w[k] >= 4 ? "hi" : ""}"><i style="width:${r.t.scores[k] * 20}%"></i></span><span>${r.t.scores[k]}/5</span>`).join("")}</div>
      ${r.reasons.length ? `<b>لماذا تناسبك:</b><ul class="why">${r.reasons.map(k => `<li>${esc(r.t.why[k])}</li>`).join("")}</ul>` : ""}
      <div class="watch">انتبه: ${esc(r.t.watch)}</div>
      <div class="vnote">آخر مراجعة: ${r.t.verify.date} · ${esc(r.t.verify.note)} · <a href="${r.t.url}" target="_blank" rel="noopener">الموقع الرسمي</a></div>
      <div class="actions"><button type="button" class="btn ${S.pick === r.t.id ? "pri" : "sec"}" data-pick="${r.t.id}">${S.pick === r.t.id ? "✓ اخترتها" : "اختر هذه الأداة"}</button></div>
    </div>`).join("")}
    <p class="hint">الأشرطة الداكنة هي المعايير الأهم لقيودك. الدرجات تقدير أولي من التوثيق وليست نتيجة اختبار عملي.</p>`;
  },
  () => {
    const tool = TOOLS.find(t => t.id === S.pick);
    const p = buildPrompt(tool);
    const plain = p.map(x => x[1]).join("\n");
    return `<h1>تعليماتك جاهزة</h1>
    <p class="lead">برومبت بعناصره الستة، مبني من بطاقة مهمتك. انسخه والصقه في ${esc(tool ? tool.name : "الأداة")}.</p>
    <div class="prompt">${p.map(x => `<span class="el">${x[0]}</span>${esc(x[1])}`).join("\n")}</div>
    <div class="actions"><button type="button" class="btn pri" id="copy">نسخ البرومبت</button><span class="hint" id="copied"></span></div>
    <textarea id="plain" hidden>${esc(plain)}</textarea>
    <p class="hint">بعض الأدوات لا تقبل برومبتًا طويلًا دفعة واحدة؛ استخدم أجزاءه في الخانات المناسبة داخل الأداة.</p>`;
  },
  () => {
    const tool = TOOLS.find(t => t.id === S.pick) || {};
    const items = ["هل تحقق الهدف؟", "هل المعلومات دقيقة؟", "هل يعمل الملف بصورة صحيحة؟", "هل النص واضح؟", "هل الروابط صحيحة؟", "هل حميت البيانات الحساسة؟", "هل يناسب المُخرَج الجمهور والجهاز؟"];
    const all = items.every((_, i) => S.checks[i]);
    return `<h1>نفّذ نسخة صغيرة… ثم تحقق</h1>
    <p class="lead">لا تعتمد أول نتيجة. نفّذ نسخة قصيرة أولًا، ثم افحصها بهذه القائمة.</p>
    <div class="card checks no-print"><h3>قائمة التحقق النهائية</h3>${items.map((t, i) =>
      `<label><input type="checkbox" data-c="${i}" ${S.checks[i] ? "checked" : ""}><span>${t}</span></label>`).join("")}
      <p class="hint">${all ? "كل الإجابات «نعم»: يمكنك اعتماد النتيجة." : "إذا كانت إجابة أي سؤال «لا»، فعدّل التعليمات وأعد التنفيذ الصغير."}</p></div>
    <div class="summary"><h3 style="margin:0;color:var(--gold)">بطاقة القرار</h3><dl>
      <dt>المهمة</dt><dd>${esc(taskSentence())}</dd>
      <dt>الأداة المختارة</dt><dd>${esc(tool.name || "")}</dd>
      <dt>التعليمات</dt><dd style="white-space:pre-wrap">${esc(buildPrompt(tool).map(x => x[1]).join("\n"))}</dd>
      <dt>طريقة التحقق</dt><dd>${all ? "اجتازت النتيجة قائمة التحقق كاملة." : "قيد التحقق."}</dd></dl></div>
    <div class="actions"><button type="button" class="btn pri" onclick="window.print()">حفظ بطاقة القرار PDF</button>
    <button type="button" class="btn sec" id="reset">مهمة جديدة</button></div>`;
  }
];

function render() {
  nav.innerHTML = STEPS.map((s, i) => `<button type="button" class="${i < S.step ? "done" : i === S.step ? "cur" : ""}" ${i <= S.step ? "" : "disabled"} data-s="${i}"><span class="dot"></span>${i + 1}. ${s}</button>`).join("");
  nav.querySelectorAll("button").forEach(b => b.addEventListener("click", () => { S.step = +b.dataset.s; save(); render(); }));
  app.innerHTML = screens[S.step]() + (S.step < 4 ? `<div class="actions">
    ${S.step > 0 ? `<button type="button" class="btn sec" id="prev">→ السابق</button>` : ""}
    <button type="button" class="btn pri" id="next">التالي ←</button>
    ${S.step < 2 ? `<span class="hint">أكمل الخانات المطلوبة للمتابعة</span>` : ""}</div>` :
    `<div class="actions no-print"><button type="button" class="btn sec" id="prev">→ السابق</button></div>`);
  bind();
  app.querySelectorAll("[data-pick]").forEach(b => b.addEventListener("click", () => { S.pick = b.dataset.pick; save(); render(); }));
  app.querySelectorAll("[data-c]").forEach(c => c.addEventListener("change", () => { S.checks[c.dataset.c] = c.checked; save(); render(); }));
  const cp = document.getElementById("copy");
  if (cp) cp.addEventListener("click", async () => {
    const v = document.getElementById("plain").value;
    try { await navigator.clipboard.writeText(v); } catch (e) { const t = document.createElement("textarea"); t.value = v; t.style.position = "fixed"; t.style.opacity = "0"; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); }
    document.getElementById("copied").textContent = "تم النسخ";
  });
  const rs = document.getElementById("reset");
  if (rs) rs.addEventListener("click", () => { S = blank(); save(); render(); window.scrollTo(0, 0); });
}
render();
