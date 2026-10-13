"""يولّد صفحات منصة مسار من data/packages.json (13 أكتوبر 2026).
التشغيل من جذر المستودع: python3 tools/build_site.py   (يحتاج: pip install markdown)
لإضافة حقيبة: أضف عنصرًا في data/packages.json ثم شغّل السكربت.
الصفحات المولّدة: index.html · packages.html · p/<slug>.html (عامة) · workshop.html · workshop/<slug>.html · workshop/doc-*.html (لصاحب المشروع)
"""
import json, os, re, html, markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'data/packages.json'), encoding='utf-8'))
E = html.escape

ICONS = {
 'box': '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>',
 'tool': '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
 'lock': '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 'play': '<circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z"/>',
 'file': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
 'quiz': '<path d="M9 11l2 2 4-4"/><rect x="3" y="3" width="18" height="18" rx="3"/>',
 'award': '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-3 5 3-1.5-7"/>',
 'book': '<path d="M4 19V5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM19 19v2H6"/>',
 'compass': '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
 'list': '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
 'image': '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 17-5-5-9 8"/>',
 'megaphone': '<path d="M3 11v2a1 1 0 0 0 1 1h3l6 4V6L7 10H4a1 1 0 0 0-1 1zM17 8a5 5 0 0 1 0 8"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'handshake': '<path d="m11 17 2 2a1.5 1.5 0 0 0 2-2M14 14l2.5 2.5a1.5 1.5 0 0 0 2-2L13 9l-2 2a2 2 0 0 1-3-3l3-3h3l5 5M3 9l4-4 4 4"/>',
 'map': '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
 'star': '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
}
def ic(name, cls=''):
    return f'<span class="ic {cls}"><svg viewBox="0 0 24 24">{ICONS[name]}</svg></span>'

SITE = 'https://gido70.github.io/Masar-AI/'
DESC = 'حقائب تطبيقية بالعربية في الذكاء الاصطناعي'
def page(title, body, pre, on, extra_head='', desc=DESC, img='assets/og-masar.png', path=''):
    nav = [('home', pre or './', 'الرئيسية'), ('packages', pre + 'packages.html', 'الحقائب'), ('tool', pre + 'tool.html', 'الأداة المجانية')]
    navh = ''.join(f'<a href="{h}"' + (' class="on"' if k == on else '') + f'>{t}</a>' for k, h, t in nav)
    navh += f'<a href="{pre}workshop.html" class="ws' + (' on' if on == 'workshop' else '') + '">🔒 الورشة</a>'
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:type" content="website"><meta property="og:locale" content="ar_AR"><meta property="og:site_name" content="مسار">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}{img}"><meta property="og:url" content="{SITE}{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{pre}assets/favicon.png">
<link rel="manifest" href="{pre}manifest.webmanifest">
<meta name="theme-color" content="#123E6B">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="مسار"><meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/site.css">{extra_head}
<script src="{pre}assets/site.js" defer></script>
</head>
<body>
<div class="bar"><div class="wrap"><a href="{pre or './'}"><img src="{pre}training/masar_logo.png" alt="مسار"></a><nav class="nav">{navh}</nav></div></div>
{body}
<footer class="ft"><div class="wrap"><span>مسار · حقائب تطبيقية في الذكاء الاصطناعي</span><span><a href="{pre}workshop.html">الورشة</a></span></div></footer>
</body>
</html>
'''

def theme(p):
    t = p['theme']; return f' style="--a:{t["a"]};--b:{t["b"]};--soft:{t["soft"]}"'

DOC_PAGES = {}
def md(path, strip_answers=False):
    s = open(os.path.join(ROOT, path), encoding='utf-8').read()
    h = markdown.markdown(s, extensions=['tables'])
    def link(m):
        u = m.group(0).rstrip('.,،)')
        tail = m.group(0)[len(u):]
        rel = re.sub(r'^https://(?:raw\.githubusercontent\.com/gido70/Masar-AI/main/|github\.com/gido70/Masar-AI/blob/main/)', '', u)
        if rel in DOC_PAGES: return f'<a href="{DOC_PAGES[rel]}">{E(DOC_PAGES[rel + "#t"])}</a>' + tail
        if rel != u: return E(rel) + tail
        return f'<a href="{u}">{u}</a>' + tail
    return re.sub(r'(?<![\"=>])https://[^\s<"]+', link, h)

def write(rel, s):
    path = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(s); print('✓', rel)

PUB = [p for p in D['packages'] if p.get('public')]

def pk_card(p, pre, href):
    return f'''<a class="card pk" href="{href}"{theme(p)}><img src="{pre}{p["cover"]}" alt="غلاف {E(p["name"])}" loading="lazy"><div class="in"><h3>{E(p["name"])}</h3><p>{E(p["tagline"])}</p><div class="chips"><span class="chip">{len(p["units"])} وحدات</span><span class="chip st">{E(p["status"])}</span><span class="chip price">{E(p["price"])}</span></div></div></a>'''


# ---------- البوابات الثلاث للمنهجية ----------
RANK = {'✅': 2, '📝': 1, '⏳': 0}
GATES = [
 ('أ', 'الفكرة والعميل', 'قبل إنتاج المحتوى', {n: '✅' for n in (1, 2, 3, 5, 6, 7, 8, 9)}),
 ('ب', 'السوق والسعر', 'قبل صفحة الهبوط والتسعير', {**{n: '📝' for n in (4, 10, 11)}, **{n: '✅' for n in (12, 15, 16)}}),
 ('ج', 'الإطلاق', 'قبل التفعيل للجمهور', {**{n: '✅' for n in (18, 19, 20, 21)}, **{n: '📝' for n in (13, 14, 17, 22, 23)}}),
]
STEP_NAMES = {}
def load_status(p):
    mp = next((d['md'] for d in p.get('docs', []) if 'method-24' in d['md']), None)
    if not mp: return None
    txt = open(os.path.join(ROOT, mp), encoding='utf-8').read()
    for n, name, st in re.findall(r'^\| (\d+) \| ([^|]+) \| (✅|📝|⏳) \|', txt, flags=re.M): STEP_NAMES[int(n)] = name.strip()
    return {int(n): st for n, _, st in re.findall(r'^\| (\d+) \| ([^|]+) \| (✅|📝|⏳) \|', txt, flags=re.M)}
def gate_report(stat):
    out = []
    for code, title, when, req in GATES:
        missing = [n for n, need in req.items() if RANK.get(stat.get(n, '⏳'), 0) < RANK[need]]
        out.append((code, title, when, not missing, missing))
    return out
def gates_html(p):
    stat = load_status(p)
    if stat is None: return ''
    rep = gate_report(stat); nxt = next((g for g in rep if not g[3]), None)
    cards = ''
    for code, title, when, ok, miss in rep:
        mtxt = 'مكتملة' if ok else 'ينقص: ' + '، '.join(f'{n} {STEP_NAMES.get(n, "")}' for n in miss)
        cards += f'<div class="card tile">{ic("award" if ok else "lock", "green" if ok else "gold")}<div><h3 style="font-size:21px;margin-top:2px">البوابة {code}: {E(title)}</h3><p style="font-size:17px;color:var(--mute)">{E(when)}</p><p>{"✅ " if ok else "⏳ "}{E(mtxt)}</p></div></div>'
    nx = f'<p class="note" style="margin-top:14px"><b>الخطوة التالية:</b> البوابة {nxt[0]} ({E(nxt[1])}): ابدأ بالخطوة {nxt[4][0]} «{E(STEP_NAMES.get(nxt[4][0], ""))}».</p>' if nxt else '<p class="note" style="margin-top:14px"><b>عبرت الحقيبة البوابات الثلاث:</b> جاهزة للإطلاق على المنهجية.</p>'
    return f'<section class="sec" id="gates"><div class="wrap"><div class="sec-h"><div><h2>مسار الحقيبة على المنهجية</h2><p>ثلاث بوابات من الخطوات الأربع والعشرين. لا تنتقل الحقيبة إلى مرحلة قبل عبور بوابتها.</p></div></div><div class="grid g3">{cards}</div>{nx}</div></section>'

# ---------- الرئيسية ----------
def build_home():
    cards = ''.join(pk_card(p, '', f'p/{p["slug"]}.html') for p in PUB)
    body = f'''<section class="hero"><div class="wrap">
<span class="kicker">حقائب تطبيقية بالعربية</span>
<h1>تعلّم طريقًا واضحًا، و<em>اخرج بعمل حقيقي</em></h1>
<p class="lead">في كل حقيبة من حقائب مسار تتعلم كيف تنجز مهمة بالذكاء الاصطناعي خطوة خطوة، وتطبّق كل خطوة على عملك أنت، حتى تخرج بنتيجة في يدك وشهادة.</p>
<div class="row"><a class="btn p" href="packages.html">تصفّح الحقائب</a><a class="btn s" href="tool.html">جرّب الأداة المجانية</a></div>
</div></section>
<section class="sec"><div class="wrap">
<div class="grid g3">
<a class="card tile" href="packages.html">{ic("box")}<div><h3>الحقائب</h3><p>اختر المسار الذي يناسب مهمتك، وشاهد ما ستتعلمه وما ستخرج به.</p></div></a>
<a class="card tile" href="tool.html">{ic("tool","gold")}<div><h3>بطاقة الفيديو في دقيقة</h3><p>ستة أسئلة بالضغط فقط، فتخرج بخطة الفيديو الخاص بك: الشكل، والأدوات، والتكلفة.</p></div></a>
<a class="card tile" href="#how">{ic("map","navy")}<div><h3>كيف تعمل الحقيبة؟</h3><p>تقرر قبل الأداة، ثم تطبّق وحدة وحدة، ثم تخرج بنتيجة وشهادة.</p></div></a>
</div></div></section>
<section class="sec"><div class="wrap">
<div class="sec-h"><div><h2>الحقائب المتاحة</h2><p>كل حقيبة بهويتها، والمنهج واحد.</p></div><a class="btn s" href="packages.html">كل الحقائب</a></div>
<div class="grid g2">{cards}</div></div></section>
<section class="sec" id="how"><div class="wrap">
<div class="sec-h"><div><h2>كيف تعمل الحقيبة؟</h2></div></div>
<div class="grid g3">
<div class="card tile">{ic("compass")}<div><h3>تقرر قبل الأداة</h3><p>تحدد مهمتك وجمهورك وقيودك في بطاقة واحدة، فلا تضيع بين عشرات الأدوات.</p></div></div>
<div class="card tile">{ic("file","gold")}<div><h3>تطبّق وحدة وحدة</h3><p>فيديو قصير، وملف بورقة عمل تكتب فيها على مهمتك، وأداة مع بديل مجاني.</p></div></div>
<div class="card tile">{ic("award","navy")}<div><h3>تخرج بنتيجة وشهادة</h3><p>امتحان قصير يفتح الوحدة التالية، وفي النهاية عمل منجز وشهادة إتمام.</p></div></div>
</div></div></section>'''
    write('index.html', page('مسار', body, '', 'home', path=''))

def build_packages():
    cards = ''.join(pk_card(p, '', f'p/{p["slug"]}.html') for p in PUB)
    soon = ' · '.join(D['soon'])
    body = f'''<section class="hero"><div class="wrap"><span class="kicker">الحقائب</span><h1>اختر <em>مسارك</em></h1><p class="lead">كل حقيبة تأخذك في طريق واضح لإنجاز مهمة محددة بالذكاء الاصطناعي، بتطبيق على عملك أنت.</p></div></section>
<section class="sec"><div class="wrap"><div class="grid g2">{cards}</div>
<p class="note" style="margin-top:22px">حقائب قيد الإعداد: {E(soon)}.</p></div></section>'''
    write('packages.html', page('الحقائب · مسار', body, '', 'packages', path='packages.html'))

# ---------- صفحة حقيبة عامة ----------
def build_public(p):
    pre = '../'
    units = ''.join(f'<li><span class="num">{u["n"]}</span><div><b>{E(u["title"])}</b><span>{E(u["q"])} · تخرج بـ: {E(u["out"])}</span></div></li>' for u in p['units'])
    gets = ''.join(f'<li>{E(g)}</li>' for g in p['gets'])
    body = f'''<div{theme(p)}>
<section class="phero"><div class="wrap"><div class="g">
<div><span class="kicker">{E(p["status"])}</span><h1>{E(p["name"])}</h1><p class="lead">{E(p["tagline"])}. {E(p["promise"])}</p>
<div class="chips"><span class="chip">{len(p["units"])} وحدات</span><span class="chip">{E(p["hours"])}</span><span class="chip">شهادة</span><span class="chip price">{E(p["price"])}</span></div></div>
<div class="vbox"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{p["promo"]}?rel=0" title="إعلان {E(p["name"])}" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
</div></div></section>
<section class="sec"><div class="wrap"><div class="grid" style="grid-template-columns:1.4fr .9fr;gap:24px">
<div><div class="sec-h"><div><h2>ماذا ستتعلم</h2><p>مخرج كل وحدة هو مدخل الوحدة التي بعدها.</p></div></div><ol class="ulist">{units}</ol></div>
<div><div class="card"><h3 style="margin-top:0">ماذا ستحصل عليه</h3><ul class="gets">{gets}</ul></div>
<div class="price-box" style="margin-top:16px"><div>السعر</div><div class="p">{E(p["price"])}</div><div style="opacity:.85;font-size:15px">{E(p["status"])}</div></div></div>
</div></div></section></div>'''
    write(f'p/{p["slug"]}.html', page(f'{p["name"]}: {p["tagline"]} · مسار', body, pre, 'packages', desc=p['promise'], img=p['cover'], path=f'p/{p["slug"]}.html'))

# ---------- الورشة ----------
def build_workshop():
    pk_tiles = ''.join(f'<a class="card tile" href="workshop/{p["slug"]}.html"{theme(p)}>{ic("box","red" if p["slug"]=="video" else "")}<div><h3>{E(p["name"])}</h3><p>الوحدات بفيديوهاتها وملفاتها وأسئلتها، والتسويق، وملفات CPS، وحالتها في المنهجية.</p></div></a>' for p in D['packages'])
    tr_tiles = ''.join(f'<a class="card tile" href="{p["trainer"]}">{ic("book","gold")}<div><h3>مسار المدرّب: {E(p["name"])}</h3><p>المفاهيم، والأسباب، وكيف بُنيت، وأسئلة الناس وأجوبتك.</p></div></a>' for p in D['packages'] if p.get('trainer'))
    body = f'''<section class="hero"><div class="wrap"><span class="kicker">لصاحب المشروع</span><h1>الورشة</h1><p class="lead">كل ما تحتاجه لإدارة الحقائب وبنائها والتأهل لتقديمها، مصنفًا في ثلاثة أقسام.</p></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>الحقائب</h2><p>ملف كامل لكل حقيبة.</p></div></div><div class="grid g2">{pk_tiles}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>التأهيل للتدريب</h2></div></div><div class="grid g2">{tr_tiles}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>إدارة المشروع</h2></div></div><div class="grid g3">
<a class="card tile" href="masar-index.html">{ic("list","navy")}<div><h3>الإندكس</h3><p>نقطة العمل الآن، والقرارات، والسجل، والنواقص.</p></div></a>
<a class="card tile" href="workshop/method.html">{ic("compass")}<div><h3>المنهجية الأربع والعشرون</h3><p>الخطوات التي تمر بها كل حقيبة، من العميل إلى الاستدامة.</p></div></a>
<a class="card tile" href="workshop/doc-rebuild.html">{ic("map","gold")}<div><h3>خارطة إعادة البناء</h3><p>مراحل إعادة بناء المنصة وقواعدها.</p></div></a>
</div></div></section>'''
    write('workshop.html', page('الورشة · مسار', body.replace('href="masar-index.html"', 'href="masar-index.html"'), '', 'workshop', '\n<meta name="robots" content="noindex">'))

def quiz_html(path):
    s = open(os.path.join(ROOT, path), encoding='utf-8').read().split('\n', 1)[1]
    return markdown.markdown(s)

def build_ws_pkg(p):
    pre = '../'
    units = ''
    for u in p['units']:
        extra = ''
        if u.get('quiz'): extra += f'<details class="more"><summary>📝 الامتحان (بالإجابات)</summary><div>{quiz_html(u["quiz"])}</div></details>'
        if u.get('text'): extra += f'<details class="more"><summary>📜 نص المحتوى</summary><div>{md(u["text"])}</div></details>'
        units += f'''<div class="card unit"><a class="th" href="https://youtu.be/{u["video"]}" data-title="الوحدة {u["n"]}: {E(u["title"])}"><img src="https://i.ytimg.com/vi/{u["video"]}/hqdefault.jpg" alt="" loading="lazy"></a>
<div><span class="n">الوحدة {u["n"]}</span><h3>{E(u["title"])}</h3><span class="out">تخرج بـ: {E(u["out"])}</span>
<div class="acts"><a href="https://youtu.be/{u["video"]}" data-title="الوحدة {u["n"]}: {E(u["title"])}">▶ الفيديو</a><a href="{pre}{u["pdf"]}" data-title="ملف الوحدة {u["n"]}: {E(u["title"])}">📄 الملف PDF</a></div>{extra}</div></div>'''
    files = ''.join(f'<a class="card tile" href="{pre}{f["href"]}" data-title="{E(f["title"])}">{ic(f["icon"],"sm gold")}<div><h3 style="font-size:19px">{E(f["title"])}</h3></div></a>' for f in p['files'])
    docs = ''
    for i, d in enumerate(p['docs']):
        slug = f'doc-{p["slug"]}-{i+1}'
        write(f'workshop/{slug}.html', page(f'{d["title"]} · {p["name"]}', f'<div class="wrap"><p class="crumb"><a href="../workshop.html">الورشة</a> ← <a href="{p["slug"]}.html">{E(p["name"])}</a></p><div class="doc" style="margin-top:12px">{md(d["md"])}</div></div>', pre, 'workshop', '\n<meta name="robots" content="noindex">'))
        docs += f'<a class="card tile" href="{slug}.html">{ic(d["icon"],"sm")}<div><h3 style="font-size:19px">{E(d["title"])}</h3></div></a>'
    tabs = ('<a href="#gates">مسار المنهجية</a>' if gates_html(p) else '') + '<a href="#units">الوحدات</a>' + ('<a href="#docs">التسويق وCPS والمنهجية</a>' if docs else '') + '<a href="#files">الملفات</a><a href="#cert">الشهادة</a>' + (f'<a href="{pre}{p["trainer"]}">مسار المدرّب</a>' if p.get('trainer') else '') + f'<a href="{pre}p/{p["slug"]}.html">الصفحة العامة</a>'
    body = f'''<div{theme(p)}>
<section class="phero"><div class="wrap"><p class="crumb" style="margin-top:0"><a href="../workshop.html">الورشة</a> ← {E(p["name"])}</p><div class="g">
<div><span class="kicker">{E(p["status"])} · {E(p["price"])}</span><h1>{E(p["name"])}</h1><p class="lead">{E(p["tagline"])}. ملف الحقيبة الكامل لصاحب المشروع.</p></div>
<div><img src="{pre}{p["cover"]}" alt="" style="width:100%;border-radius:20px;box-shadow:0 20px 40px rgba(0,0,0,.15)"></div></div></div></section>
<div class="tabs"><div class="wrap">{tabs}</div></div>
{gates_html(p)}
<section class="sec" id="units"><div class="wrap"><div class="sec-h"><div><h2>الوحدات</h2><p>الفيديو، والملف، والامتحان بإجاباته، ونص المحتوى.</p></div></div><div class="grid">{units}</div></div></section>
{f'<section class="sec" id="docs"><div class="wrap"><div class="sec-h"><div><h2>التسويق وCPS والمنهجية</h2></div></div><div class="grid g2">{docs}</div></div></section>' if docs else ''}
<section class="sec" id="files"><div class="wrap"><div class="sec-h"><div><h2>الملفات</h2></div></div><div class="grid g3">{files}</div></div></section>
<section class="sec" id="cert"><div class="wrap"><div class="sec-h"><div><h2>الشهادة</h2></div></div><img src="{pre}{p["certificate"]}" alt="الشهادة" style="width:100%;max-width:820px;border-radius:16px;box-shadow:0 14px 30px rgba(0,0,0,.12)"></div></section>
</div>'''
    write(f'workshop/{p["slug"]}.html', page(f'ملف {p["name"]} · الورشة', body, pre, 'workshop', '\n<meta name="robots" content="noindex">'))

def build_method():
    pre = '../'
    s = open(os.path.join(ROOT, 'docs/METHOD-24.md'), encoding='utf-8').read()
    axes = re.split(r'^## ', s, flags=re.M)[1:]
    colors = ['', 'gold', 'navy', 'green', 'red', 'ink']
    icons = ['star', 'box', 'megaphone', 'award', 'tool', 'map']
    blocks = ''
    for i, a in enumerate(axes):
        title, rest = a.split('\n', 1)
        rows = re.findall(r'^\| (\d+) \| ([^|]+) \| ([^|]+) \|', rest, flags=re.M)
        if not rows: continue
        items = ''.join(f'<li><span class="num">{n}</span><div><b>{E(t.strip())}</b><span>{E(q.strip())}</span></div></li>' for n, t, q in rows)
        blocks += f'<div class="card"><div class="tile">{ic(icons[i%6], colors[i%6])}<div><h3 style="margin-top:4px">{E(title.strip())}</h3></div></div><ol class="ulist" style="margin-top:14px">{items}</ol></div>'
    # مصفوفة الحالة: كل خطوة × كل حقيبة
    stat = {}
    for p in D['packages']:
        mp = next((d['md'] for d in p['docs'] if 'method-24' in d['md']), None)
        if not mp: continue
        rows = re.findall(r'^\| (\d+) \| [^|]+ \| (✅|📝|⏳) \|', open(os.path.join(ROOT, mp), encoding='utf-8').read(), flags=re.M)
        stat[p['slug']] = {int(n): st for n, st in rows}
    pk = [p for p in D['packages'] if p['slug'] in stat]
    names = {}
    for a in axes:
        for n, t, q in re.findall(r'^\| (\d+) \| ([^|]+) \| ([^|]+) \|', a, flags=re.M): names[int(n)] = t.strip()
    head = ''.join(f'<th><a href="doc-{p["slug"]}-1.html" style="color:#fff">{E(p["name"])}</a></th>' for p in pk)
    body_rows = ''.join(f'<tr><td>{n}</td><td>{E(names.get(n, ""))}</td>' + ''.join(f'<td style="text-align:center;font-size:20px">{stat[p["slug"]].get(n, "·")}</td>' for p in pk) + '</tr>' for n in range(1, 25))
    totals = ''.join(f'<div class="card tile"{theme(p)}>{ic("compass","sm")}<div><h3 style="font-size:19px">{E(p["name"])}</h3><p>✅ {list(stat[p["slug"]].values()).count("✅")} · 📝 {list(stat[p["slug"]].values()).count("📝")} · ⏳ {list(stat[p["slug"]].values()).count("⏳")}</p><p>البوابات: {" · ".join(("✅ " if g[3] else "⏳ ") + g[0] for g in gate_report(stat[p["slug"]]))} · <a href="{p["slug"]}.html#gates">التفاصيل</a></p></div></div>' for p in pk)
    status = f'<div class="grid g2">{totals}</div><div class="doc" style="margin-top:18px"><h2 style="margin-top:0">مسار الحقائب على المنهجية</h2><table><tr><th>#</th><th>الخطوة</th>{head}</tr>{body_rows}</table></div>'
    body = f'''<section class="hero"><div class="wrap"><p class="crumb" style="margin-top:0"><a href="../workshop.html">الورشة</a> ← المنهجية</p><span class="kicker">لكل حقيبة</span><h1>المنهجية الأربع والعشرون</h1><p class="lead">خطوات «مخيم صناعة المنتج الرقمي» التي بُنيت بها الحقيبة الأولى. كل حقيبة جديدة تجيب عن سؤال كل خطوة، وتُسجَّل حالتها: ✅ منفذة · 📝 موثقة فقط · ⏳ لم تبدأ.</p></div></section>
<section class="sec"><div class="wrap">{status}</div></section>
<section class="sec"><div class="wrap"><div class="grid g2">{blocks}</div></div></section>'''
    write('workshop/method.html', page('المنهجية الأربع والعشرون · الورشة', body, pre, 'workshop', '\n<meta name="robots" content="noindex">'))
    write('workshop/doc-rebuild.html', page('خارطة إعادة البناء · الورشة', f'<div class="wrap"><p class="crumb"><a href="../workshop.html">الورشة</a> ← خارطة إعادة البناء</p><div class="doc" style="margin-top:12px">{md("docs/PLATFORM-REBUILD.md")}</div></div>', pre, 'workshop', '\n<meta name="robots" content="noindex">'))


# ---------- الأداة المجانية: بطاقة الفيديو في دقيقة ----------
TOOL_JS = r"""
const Q=[
 {k:'purpose',t:'ما غرض الفيديو؟',o:[['lesson','درس تعليمي'],['software','شرح برنامج أو موقع'],['ad','إعلان أو ترويج'],['short','محتوى قصير للتواصل'],['org','تعريف بجهة أو مشروع'],['interview','مقابلة أو شهادة عميل'],['event','ملخص فعالية'],['story','قصة'],['greet','تهنئة أو مناسبة'],['translate','ترجمة فيديو موجود']]},
 {k:'where',t:'أين سيُشاهَد غالبًا؟',o:[['phone','على الهاتف'],['youtube','على يوتيوب أو الحاسوب'],['hall','على شاشة قاعة']]},
 {k:'level',t:'من جمهورك؟',o:[['new','مبتدئون في الموضوع'],['mid','لديهم خلفية أساسية'],['pro','متخصصون']]},
 {k:'dur',t:'كم مدة الفيديو؟',o:[['30','نصف دقيقة'],['60','دقيقة'],['120','دقيقتان'],['300','خمس دقائق']]},
 {k:'voice',t:'بأي صوت؟',o:[['mine','بصوتي'],['ai','صوت مولّد بالذكاء الاصطناعي'],['none','بلا تعليق، نص على الشاشة']]},
 {k:'budget',t:'كم تريد أن تدفع؟',o:[['free','لا شيء، مجاني تمامًا'],['low','حتى 5 دولارات'],['more','أكثر إن لزم']]}
];
const SHAPE={lesson:'slides',software:'screen',ad:'ai',short:'camera',org:'footage',interview:'camera',event:'footage',story:'photos',greet:'photos',translate:'dub'};
const FREE_ALT={ai:'photos',avatar:'slides'};
const S={slides:['شرائح مع صوت','مجاني','Canva أو PowerPoint','Google Slides'],screen:['تسجيل الشاشة','مجاني','OBS Studio','مسجّل الشاشة في جهازك'],camera:['أمام الكاميرا','مجاني','كاميرا الهاتف','كاميرا الهاتف'],footage:['مونتاج لقطات','مجاني','CapCut','DaVinci Resolve'],photos:['صور متحركة','مجاني إلى سنتات','CapCut','CapCut'],ai:['مشاهد مولّدة بالذكاء الاصطناعي','الأغلى','Runway أو Kling','صور متحركة بـ CapCut'],avatar:['أفاتار (مقدّم رقمي)','الأغلى','HeyGen أو Synthesia','شرائح مع صوتك'],dub:['ترجمة أو دبلجة','مجاني إلى الأغلى','CapCut (ترجمة تلقائية)','YouTube Studio']};
const VOICE={mine:['صوتك بالهاتف','مجاني','الهاتف + Audacity للتنظيف'],ai:['صوت مولّد','سنتات','ElevenLabs'],none:['بلا تعليق','مجاني','النص على الشاشة يحمل الرسالة']};
let A={},i=0;
const $=s=>document.querySelector(s);
function draw(){
  const box=$('#q');
  if(i>=Q.length){return result();}
  const q=Q[i];
  $('#dots').innerHTML=Q.map((_,j)=>`<i class="${j<i?'d':j===i?'c':''}"></i>`).join('');
  box.innerHTML=`<div class="qn">السؤال ${i+1} من ${Q.length}</div><h2>${q.t}</h2><div class="opts">${q.o.map(([v,l])=>`<button type="button" data-v="${v}" class="${A[q.k]===v?'on':''}">${l}</button>`).join('')}</div>${i?'<button type="button" class="back" id="back">→ السابق</button>':''}`;
  box.querySelectorAll('.opts button').forEach(b=>b.onclick=()=>{A[q.k]=b.dataset.v;i++;draw();});
  const bk=$('#back'); if(bk) bk.onclick=()=>{i--;draw();};
}
function result(){
  $('#dots').innerHTML='';
  let sh=SHAPE[A.purpose];
  if(A.purpose==='short'&&A.budget!=='free'&&A.voice==='ai') sh='avatar';
  let note='';
  if(A.budget==='free'&&FREE_ALT[sh]){note=`الشكل الأمثل لغرضك «${S[sh][0]}»، لكنه مدفوع، فاخترنا لك بديلًا مجانيًا.`;sh=FREE_ALT[sh];}
  const s=S[sh], d=+A.dur, words=Math.round(d*1.8);
  const frame=A.where==='phone'?'عمودي 9:16':'أفقي 16:9';
  const v=VOICE[A.voice];
  let cost='مجاني'; if(sh==='avatar'){cost=`نحو ${(d*0.06).toFixed(1)} دولار للمقدّم (6 سنتات للثانية تقريبًا)`;} else if(sh==='ai'){cost='عدة دولارات (يُحسب بالثانية؛ جرّب لقطة قصيرة أولًا)';} else if(A.voice==='ai'){cost='سنتات (للصوت المولّد)';}
  const lvl={new:'اشرح كل مصطلح، ومثالًا لكل فكرة',mid:'ادخل في الفكرة مباشرة',pro:'ركّز على الجديد والتفاصيل الدقيقة'}[A.level];
  const rows=[['الشكل الأنسب',s[0]],['الإطار',frame],['عدد الكلمات',`نحو ${words} كلمة (${d} ثانية × 1.8)`],['الصوت',`${v[0]} · ${v[2]}`],['الأدوات',`${s[2]} · البديل المجاني: ${s[3]}`],['المونتاج','CapCut · البديل: DaVinci Resolve'],['التكلفة المتوقعة',cost],['أسلوب الشرح',lvl]];
  window._card=rows.map(r=>r[0]+': '+r[1]).join('\n');
  $('#q').innerHTML=`<div class="qn">بطاقتك جاهزة</div><h2>خطة الفيديو الخاص بك</h2>${note?`<p class="note">${note}</p>`:''}
  <div class="res">${rows.map(r=>`<div><span>${r[0]}</span><b>${r[1]}</b></div>`).join('')}</div>
  <h3>ثلاث خطوات تبدأ بها الآن</h3><ol class="steps"><li>اكتب رسالة واحدة يخرج بها المشاهد.</li><li>اكتب النص في نحو ${words} كلمة، بجمل قصيرة تُفهم من سماعها.</li><li>اصنع الصوت أولًا، ثم المشاهد على مدته.</li></ol>
  <div class="row"><button type="button" class="btn p" id="copy">انسخ البطاقة</button><button type="button" class="btn s" id="again">ابدأ من جديد</button></div>
  <div class="cta"><b>تريد الطريق كاملًا خطوة خطوة؟</b><span>حقيبة «مسار الفيديو» تأخذك من هذه البطاقة إلى فيديو منشور، في ست وحدات.</span><a class="btn p" href="p/video.html">تعرّف على الحقيبة</a></div>`;
  $('#copy').onclick=()=>{navigator.clipboard&&navigator.clipboard.writeText(window._card);$('#copy').textContent='نُسخت ✓';};
  $('#again').onclick=()=>{A={};i=0;draw();};
}
draw();
"""

def build_tool():
    body = f"""<section class="hero" style="padding-bottom:10px"><div class="wrap"><span class="kicker">أداة مجانية · دقيقة واحدة</span><h1>بطاقة <em>الفيديو</em> في دقيقة</h1><p class="lead">ستة أسئلة بالضغط فقط، بلا كتابة. تخرج بخطة الفيديو الخاص بك: الشكل الأنسب، والإطار، وعدد الكلمات، والأدوات، والتكلفة.</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap"><div class="card tool"><div class="dots" id="dots"></div><div id="q"></div></div></div></section>
<style>
.tool{{max-width:760px;margin:0 auto;padding:26px}}
.dots{{display:flex;gap:6px;justify-content:center;margin-bottom:14px}}.dots i{{width:34px;height:6px;border-radius:3px;background:var(--line)}}.dots i.d{{background:var(--teal)}}.dots i.c{{background:var(--gold)}}
.qn{{text-align:center;color:var(--mute);font-weight:700;font-size:15px}}
.tool h2{{text-align:center;font-size:30px;margin:6px 0 18px}}
.opts{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}
.opts button{{font:inherit;font-weight:700;font-size:18px;padding:16px;border-radius:16px;border:2px solid var(--line);background:#fff;color:var(--navy);cursor:pointer;box-shadow:0 4px 0 var(--line);transition:transform .1s}}
.opts button:hover,.opts button.on{{border-color:var(--teal);box-shadow:0 4px 0 var(--teal)}}
.opts button:active{{transform:translateY(3px);box-shadow:0 1px 0 var(--teal)}}
.back{{display:block;margin:16px auto 0;background:none;border:0;color:var(--mute);font:inherit;font-weight:700;cursor:pointer}}
.res{{display:grid;gap:8px;margin:10px 0 18px}}.res div{{display:grid;grid-template-columns:150px 1fr;gap:12px;background:var(--soft);border-radius:12px;padding:10px 14px}}.res span{{color:var(--mute);font-weight:700}}.res b{{color:var(--navy)}}
.tool h3{{font-size:21px;margin:10px 0 6px}}.steps{{margin:0 0 18px;padding-inline-start:22px}}
.cta{{margin-top:20px;background:linear-gradient(150deg,#1B1B2F,#3a1010);color:#fff;border-radius:18px;padding:18px;display:grid;gap:8px}}.cta b{{font-size:20px}}.cta .btn{{justify-self:start}}
@media (max-width:620px){{.opts{{grid-template-columns:1fr}}.res div{{grid-template-columns:1fr;gap:2px}}}}
</style>
<script>{TOOL_JS}</script>"""
    write('tool.html', page('بطاقة الفيديو في دقيقة · أداة مجانية · مسار', body, '', 'tool', desc='ستة أسئلة بالضغط فقط تعطيك خطة الفيديو الخاص بك: الشكل الأنسب، والإطار، وعدد الكلمات، والأدوات، والتكلفة.', path='tool.html'))

def redirects():
    for old, new in (('video-package.html', 'p/video.html'), ('package.html', 'p/free.html'), ('home-new.html', './')):
        write(old, f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{new}"><a href="{new}">انتقل</a>')

if __name__ == '__main__':
    for p in D['packages']:
        for i, d in enumerate(p['docs']): DOC_PAGES[d['md']] = f'doc-{p["slug"]}-{i+1}.html'; DOC_PAGES[d['md'] + '#t'] = d['title']
    build_home(); build_packages()
    for p in PUB: build_public(p)
    build_workshop()
    for p in D['packages']: build_ws_pkg(p)
    build_method(); build_tool(); redirects()
    for p in PUB:
        st = load_status(p)
        if st and not gate_report(st)[2][3]: print(f'⚠ {p["name"]}: معروضة للجمهور ولم تعبر البوابة ج (الإطلاق) بعد')
