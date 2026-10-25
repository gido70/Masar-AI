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
<div class="chips"><span class="chip">{len(p["units"])} وحدات</span><span class="chip">{E(p["hours"])}</span>{'<span class="chip">شهادة</span>' if p.get("certificate") else ''}<span class="chip price">{E(p["price"])}</span></div></div>
{f'<div class="vbox"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{p["promo"]}?rel=0" title="إعلان {E(p["name"])}" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>' if p.get("promo") else f'<div class="vbox"><img src="{pre}{p["cover"]}" alt="غلاف {E(p["name"])}" style="width:100%;height:100%;object-fit:cover"></div>'}
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
    lec_tiles = ''
    for p in D['packages']:
        L = p.get('lecture')
        if not L: continue
        nslug = f'doc-{p["slug"]}-lecture-notes'
        write(f'workshop/{nslug}.html', page(f'ملاحظات محاضرة {p["name"]}', f'<div class="wrap"><p class="crumb"><a href="../workshop.html">الورشة</a> ← ملاحظات المتحدث</p><div class="doc" style="margin-top:12px">{md(L["notes"])}</div></div>', '../', 'workshop', '\n<meta name="robots" content="noindex">'))
        lec_tiles += f'<div class="card"{theme(p)}><div class="tile">{ic("play","red" if p["slug"]=="video" else "navy")}<div><h3>محاضرة {E(p["name"])}</h3><p>{E(L["title"])} · {E(L["date"])}</p></div></div><div class="acts" style="margin-top:14px"><a href="{L["href"]}" data-out target="_blank" rel="noopener">▶ العرض التفاعلي</a><a href="{L["pdf"]}" data-title="محاضرة {E(p["name"])}">📄 نسخة PDF</a><a href="{L["pptx"]}" download data-out>⬇ PowerPoint</a><a href="workshop/{nslug}.html">📝 ملاحظات المتحدث</a></div></div>'
    body = f'''<section class="hero"><div class="wrap"><span class="kicker">لصاحب المشروع</span><h1>الورشة</h1><p class="lead">كل ما تحتاجه لإدارة الحقائب وبنائها والتأهل لتقديمها، مصنفًا في ثلاثة أقسام.</p></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>الحقائب</h2><p>ملف كامل لكل حقيبة.</p></div></div><div class="grid g2">{pk_tiles}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>التأهيل للتدريب</h2></div></div><div class="grid g2">{tr_tiles}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>المحاضرات والعروض</h2><p>عروض المحاضرات بملاحظات المتحدث، تفتح في Claude ويمكن تنزيلها PowerPoint.</p></div></div><div class="grid g2">{lec_tiles}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-h"><div><h2>إدارة المشروع</h2></div></div><div class="grid g3">
<a class="card tile" href="masar-index.html">{ic("list","navy")}<div><h3>الإندكس</h3><p>نقطة العمل الآن، والقرارات، والسجل، والنواقص.</p></div></a>
<a class="card tile" href="workshop/free-workbook.html">{ic("file","navy")}<div><h3>الكراسة التفاعلية: المجانية</h3><p>بأمثلة جاهزة ونموذج محلول، للشرح في المحاضرة.</p></div></a>
<a class="card tile" href="workshop/video-workbook.html">{ic("file","red")}<div><h3>أوراق العمل التفاعلية: الفيديو</h3><p>ست أوراق بأمثلة جاهزة ونموذج محلول.</p></div></a>
<a class="card tile" href="training/">{ic("quiz","gold")}<div><h3>الاختبارات</h3><p>كل اختبارات الحقائب في مكان واحد، مع مفتاح الإجابات.</p></div></a>
<a class="card tile" href="workshop/method.html">{ic("compass")}<div><h3>المنهجية الأربع والعشرون</h3><p>الخطوات التي تمر بها كل حقيبة، من العميل إلى الاستدامة.</p></div></a>
<a class="card tile" href="workshop/doc-rebuild.html">{ic("map","gold")}<div><h3>خارطة إعادة البناء</h3><p>مراحل إعادة بناء المنصة وقواعدها.</p></div></a>
</div></div></section>'''
    write('workshop.html', page('الورشة · مسار', body.replace('href="masar-index.html"', 'href="masar-index.html"'), '', 'workshop', '\n<meta name="robots" content="noindex">'))

def quiz_html(path):
    s = open(os.path.join(ROOT, path), encoding='utf-8').read().split('\n', 1)[1]
    return markdown.markdown(s)

import sys as _sys; _sys.path.insert(0, os.path.join(ROOT, 'packages/ads/units'))
PAGES = json.load(open(os.path.join(ROOT, 'assets/pdfpages/index.json'), encoding='utf-8')) if os.path.exists(os.path.join(ROOT, 'assets/pdfpages/index.json')) else {}

def parse_quiz(path):
    s = open(os.path.join(ROOT, path), encoding='utf-8').read()
    qs = []
    for block in re.split(r'\n(?=\*\*\d+\.)', s)[1:]:
        q = re.match(r'\*\*\d+\.\s*(.+?)\*\*', block)
        opts = re.findall(r'^- (✅ )?(.+)$', block, flags=re.M)
        if q and opts:
            qs.append({'q': q.group(1).strip(), 'o': [o[1].strip() for o in opts], 'a': next(i for i, o in enumerate(opts) if o[0])})
    return qs

PLAYER_JS = r"""
const U=JSON.parse(document.getElementById('udata').textContent);
let cur=0,tab='pdf';
const $=s=>document.querySelector(s);
function nav(){document.querySelectorAll('.cp-list button').forEach((b,i)=>b.classList.toggle('on',i===cur));}
function show(i){
  cur=i;nav();const u=U[i];
  $('#cp-n').textContent='الوحدة '+u.n;$('#cp-t').textContent=u.title;$('#cp-o').textContent='تخرج بـ: '+u.out;
  $('#cp-v').innerHTML=u.video?'<iframe src="https://www.youtube-nocookie.com/embed/'+u.video+'?rel=0" title="'+u.title+'" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>':'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:var(--soft);color:var(--b);font-size:24px">🛠 الوحدة قيد البناء</div>';
  {const t=u.terms||[];$('#cp-terms').style.display=t.length?'':'none';$('#cp-terms').open=false;$('#cp-terms-s').textContent='📖 قبل المشاهدة: كلمات هذه الوحدة بلغة بسيطة ('+t.length+')';$('#cp-terms-b').innerHTML=t.map(x=>'<div style="margin-bottom:6px"><b>'+x[0]+':</b> '+x[1]+'</div>').join('');}
  $('#cp-yt').style.display=u.video?'':'none';$('#cp-yt').href='https://youtu.be/'+u.video;$('#cp-dl').style.display=u.pdf?'':'none';$('#cp-dl').href=u.pdf;
  document.querySelectorAll('.cp-tabs button').forEach(b=>{const k=b.dataset.k;b.style.display=(k==='quiz'&&!u.quiz.length)||(k==='text'&&!u.text)||(k==='tang'&&!u.tang)?'none':'';});
  if((tab==='quiz'&&!u.quiz.length)||(tab==='text'&&!u.text)||(tab==='tang'&&!u.tang)) tab='pdf';
  pane();
  if(location.hash!=='#u'+u.n) history.replaceState(null,'','#u'+u.n);
}
function pane(){
  document.querySelectorAll('.cp-tabs button').forEach(b=>b.classList.toggle('on',b.dataset.k===tab));
  const u=U[cur],box=$('#cp-p');
  if(tab==='pdf'&&!u.pdf){box.innerHTML='<p class="cp-tip">لا يوجد ملف لهذه الوحدة بعد.</p>';}
  else if(tab==='pdf'){
    box.innerHTML='<p class="cp-tip">للكتابة في خانات الملف: نزّله بزر «تنزيل الملف» وافتحه في Adobe Acrobat Reader.</p>';
    if(navigator.pdfViewerEnabled){box.insertAdjacentHTML('beforeend','<iframe class="cp-pdf" src="'+u.pdf+'#view=FitH"></iframe>');}
    else{let h='<div class="cp-pages">';for(let k=1;k<=u.pages;k++){h+='<img loading="lazy" src="'+u.pdir+'/'+String(k).padStart(2,'0')+'.jpg" alt="صفحة '+k+'">';}box.insertAdjacentHTML('beforeend',h+'</div>');}
  }else if(tab==='tang'){const g=u.tang,c=(h,x,col)=>'<div style="background:var(--soft);border-radius:14px;padding:14px 18px;margin-bottom:12px"><b style="color:'+(col||'var(--a)')+';font-size:19px">'+h+'</b><div style="margin-top:6px;line-height:1.7">'+x+'</div></div>';
    box.innerHTML='<div class="cp-tang"><p style="margin:0 0 12px;line-height:1.7">هنا تطبّق ما تعلّمته بيدك، خطوة صغيرة في كل وحدة. ونبني معك من الوحدة 0 إلى الوحدة 6 إعلانًا واحدًا لمقهى متخيَّل اسمه «سَمَر»، فترى في كل وحدة أين وصل.</p>'+(g.clip?'<figure style="margin:0 0 14px"><video src="'+g.clip+'" controls playsinline preload="metadata" style="width:100%;border-radius:14px;background:#000"></video><figcaption class="cp-tip" style="margin-top:6px">'+g.cap+'</figcaption></figure>':'')+c('1. أين وصل إعلان «سَمَر»؟',g.stage)+c('2. اصنع بيدك (مجانًا)',g.make,'#1F7A4D')+c('3. جرّبه على شخص آخر',g.test)+c('4. خذه معك إلى الوحدة التالية',g.carry)+'<p class="cp-tip">اكتب إجاباتك في الصفحة الأخيرة من ملف الوحدة.</p></div>';
  }else if(tab==='quiz'){quiz(u,box);}
  else{box.innerHTML='<div class="cp-text">'+u.text+'</div>';}
}
function quiz(u,box){
  const sel={};let sent=false;const N=u.quiz.length;
  box.innerHTML='<div class="cp-quiz"><p class="cp-tip">اختر إجابة لكل سؤال، وغيّرها كما تشاء، ثم اضغط «أرسل الإجابات». بعد الإرسال تُثبَّت الإجابات وتظهر النتيجة.</p>'+u.quiz.map((q,qi)=>'<div class="qz" data-q="'+qi+'"><b>'+(qi+1)+'. '+q.q+'</b><div class="qo">'+q.o.map((o,oi)=>'<button type="button" data-i="'+oi+'">'+o+'</button>').join('')+'</div></div>').join('')+'<div class="qbar"><button type="button" class="btn p" id="qsend" disabled>أرسل الإجابات (0 من '+N+')</button><button type="button" class="btn s" id="qr" style="display:none">أعد المحاولة</button><button type="button" class="btn s" id="qkey">🔑 مفتاح الإجابات</button></div><p class="qs" id="qs"></p></div>';
  const send=$('#qsend');
  box.querySelectorAll('.qz').forEach(z=>z.querySelectorAll('.qo button').forEach(b=>b.onclick=()=>{
    if(sent)return;const qi=+z.dataset.q;sel[qi]=+b.dataset.i;
    z.querySelectorAll('.qo button').forEach(x=>x.classList.toggle('sel',x===b));
    const n=Object.keys(sel).length;send.textContent='أرسل الإجابات ('+n+' من '+N+')';send.disabled=n<N;
  }));
  send.onclick=()=>{
    if(sent)return;sent=true;let ok=0;
    u.quiz.forEach((q,qi)=>{const z=box.querySelector('.qz[data-q="'+qi+'"]');const bs=z.querySelectorAll('.qo button');bs.forEach(x=>{x.classList.remove('sel');x.disabled=true;});
      if(sel[qi]===q.a){ok++;bs[q.a].classList.add('ok');}else{bs[sel[qi]].classList.add('no');bs[q.a].classList.add('ok');}});
    const pct=Math.round(ok/N*100);$('#qs').innerHTML=(pct>=80?'✅ ناجح: ':'⏳ لم تبلغ 80%: ')+ok+' من '+N+' ('+pct+'%)'+(pct>=80?' · تُفتح الوحدة التالية':' · راجع الوحدة وأعد المحاولة');
    send.style.display='none';$('#qr').style.display='';$('#qs').scrollIntoView({behavior:'smooth',block:'center'});
  };
  $('#qr').onclick=()=>quiz(u,box);
  $('#qkey').onclick=()=>{sent=true;u.quiz.forEach((q,qi)=>{const bs=box.querySelectorAll('.qz[data-q="'+qi+'"] .qo button');bs.forEach(x=>{x.classList.remove('sel','no');x.disabled=true;});bs[q.a].classList.add('ok');});
    $('#qs').textContent='🔑 الإجابات الصحيحة مظللة بالأخضر (للمدرب).';send.style.display='none';$('#qkey').style.display='none';$('#qr').style.display='';};
}
document.querySelectorAll('.cp-list button').forEach((b,i)=>b.onclick=()=>{show(i);if(innerWidth<900)$('#cp-main').scrollIntoView({behavior:'smooth'});});
document.querySelectorAll('.cp-tabs button').forEach(b=>b.onclick=()=>{tab=b.dataset.k;pane();});
$('#cp-prev').onclick=()=>show((cur-1+U.length)%U.length);$('#cp-next').onclick=()=>show((cur+1)%U.length);
const h=location.hash.match(/^#u(\d+)/);show(h?Math.max(0,U.findIndex(u=>u.n==+h[1])):Math.max(0,U.findIndex(u=>u.video)));
"""


def cps_html(p):
    c = p.get('cps')
    if not c: return ''
    rows = ''.join(f'<tr><td>{E(f["title"])}</td><td><a href="../{f["local"]}" data-title="{E(f["title"])}">النسخة المحلية</a></td><td style="direction:ltr;text-align:left;font-size:14px"><a href="{f["url"]}" data-out target="_blank" rel="noopener">{E(f["url"].split("/")[-1])}</a></td></tr>' for f in c['files'])
    return f'<section class="sec" id="cps"><div class="wrap"><div class="sec-h"><div><h2>نسخة منصة CPS</h2><p>الدورة {E(c["id"])} · {E(c["status"])} · ما يخص CPS وحده، ولا يغيّر طريقة منصة مسار.</p></div></div><p class="note">{E(c["note"])}</p><div class="doc" style="margin-top:12px"><table><tr><th>الملف</th><th>في منصة مسار</th><th>الرابط في CPS (مستودع الملفات)</th></tr>{rows}</table></div></div></section>'

def build_ws_pkg(p):
    pre = '../'
    data = []
    for u in p['units']:
        pinfo = PAGES.get(u.get('pdf', ''), {'dir': '', 'pages': 0})
        data.append({'n': u['n'], 'title': u['title'], 'out': u['out'], 'video': u.get('video', ''), 'pdf': pre + u['pdf'] if u.get('pdf') else '', 'pdir': pre + pinfo['dir'], 'pages': pinfo['pages'],
                     'quiz': parse_quiz(u['quiz']) if u.get('quiz') else [], 'text': md(u['text']) if u.get('text') else '',
                     'terms': (__import__('importlib').import_module('glossary').TERMS.get(u['n'], []) if p.get('slug') == 'ads' and u.get('video') else []), 'tang': ({**u['tangible'], 'clip': pre + u['tangible']['clip'] if u['tangible'].get('clip') else ''} if u.get('tangible') else None)})
    items = ''.join((f'<button type="button"><img src="https://i.ytimg.com/vi/{u["video"]}/mqdefault.jpg" alt="" loading="lazy">' if u.get('video') else '<button type="button" class="wip"><span style="display:flex;align-items:center;justify-content:center;min-height:56px;background:var(--soft);border-radius:8px;font-size:14px">🛠 قيد البناء</span>') + f'<span><small>الوحدة {u["n"]}</small>{E(u["title"])}</span></button>' for u in p['units'])
    files = ''.join(f'<a class="card tile" href="{pre}{f["href"]}" data-title="{E(f["title"])}">{ic(f["icon"],"sm gold")}<div><h3 style="font-size:21px">{E(f["title"])}</h3></div></a>' for f in p['files'])
    docs = ''
    for i, d in enumerate(p['docs']):
        slug = f'doc-{p["slug"]}-{i+1}'
        write(f'workshop/{slug}.html', page(f'{d["title"]} · {p["name"]}', f'<div class="wrap"><p class="crumb"><a href="../workshop.html">الورشة</a> ← <a href="{p["slug"]}.html">{E(p["name"])}</a></p><div class="doc" style="margin-top:12px">{md(d["md"])}</div></div>', pre, 'workshop', '\n<meta name="robots" content="noindex">'))
        docs += f'<a class="card tile" href="{slug}.html">{ic(d["icon"],"sm")}<div><h3 style="font-size:21px">{E(d["title"])}</h3></div></a>'
    tabs = '<a href="#player">الوحدات</a>' + (f'<a href="{p["slug"]}-workbook.html">✍️ الكراسة التفاعلية</a>' if os.path.exists(os.path.join(ROOT, f'data/workbooks/{p["slug"]}.json')) else '') + ('<a href="#gates">مسار المنهجية</a>' if gates_html(p) else '') + ('<a href="#docs">التسويق وCPS</a>' if docs else '') + ('<a href="#files">الملفات</a>' if files else '') + ('<a href="#cps">نسخة CPS</a>' if p.get('cps') else '') + ('<a href="#cert">الشهادة</a>' if p.get('certificate') else '') + (f'<a href="{pre}{p["trainer"]}">مسار المدرّب</a>' if p.get('trainer') else '') + f'<a href="{pre}p/{p["slug"]}.html">الصفحة العامة</a>'
    has_quiz = any(u.get('quiz') for u in p['units']); has_text = any(u.get('text') for u in p['units'])
    body = f"""<div{theme(p)}>
<section class="phero" style="padding:26px 0 18px"><div class="wrap"><p class="crumb" style="margin-top:0"><a href="../workshop.html">الورشة</a> ← {E(p["name"])}</p>
<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap"><img src="{pre}{p["cover"]}" alt="" style="width:220px;border-radius:14px;box-shadow:0 10px 24px rgba(0,0,0,.15)"><div><span class="kicker">{E(p["status"])} · {E(p["price"])}</span><h1 style="font-size:40px">{E(p["name"])}</h1><p class="lead" style="margin:0">{E(p["tagline"])}</p></div></div></div></section>
<div class="tabs"><div class="wrap">{tabs}</div></div>
<section class="sec" id="player"><div class="wrap">{f'<details class="cp-intro" open style="background:var(--soft);border-radius:16px;padding:12px 16px;margin:0 0 16px"><summary style="cursor:pointer;font-weight:700;color:var(--a)">🎬 ابدأ من هنا: تعرّف على سراج، مقدّم الحقيبة ({E(p["intro"]["len"])})</summary><div class="vbox" style="margin-top:10px"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{p["intro"]["video"]}?rel=0" title="مقدمة {E(p["name"])}" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div></details>' if p.get("intro") else ''}<div class="cp">
<aside class="cp-list">{items}</aside>
<div class="cp-main" id="cp-main">
<div class="cp-head"><span class="n" id="cp-n"></span><h2 id="cp-t"></h2><span class="out" id="cp-o"></span></div>
<details class="cp-terms" id="cp-terms" style="display:none;background:var(--soft);border-radius:14px;padding:10px 16px;margin:0 0 12px"><summary style="cursor:pointer;font-weight:700;color:var(--a)" id="cp-terms-s"></summary><div id="cp-terms-b" style="margin-top:8px;line-height:1.7"></div></details>
<div class="cp-v" id="cp-v"></div>
<div class="cp-bar"><button type="button" class="btn s" id="cp-next">الوحدة التالية ←</button><button type="button" class="btn s" id="cp-prev">→ السابقة</button><a class="cp-link" id="cp-dl" download>⬇ تنزيل الملف</a><a class="cp-link" id="cp-yt" data-out target="_blank" rel="noopener">افتح في يوتيوب</a></div>
<div class="cp-tabs">{'<button type="button" data-k="tang">✋ طبّق الآن</button>' if any(u.get('tangible') for u in p['units']) else ''}<button type="button" data-k="pdf">📄 الملف</button>{'<button type="button" data-k="quiz">📝 الامتحان</button>' if has_quiz else ''}{'<button type="button" data-k="text">📜 نص المحتوى</button>' if has_text else ''}</div>
<div class="cp-p" id="cp-p"></div>
</div></div></div></section>
{gates_html(p)}
{f'<section class="sec" id="docs"><div class="wrap"><div class="sec-h"><div><h2>التسويق وCPS</h2></div></div><div class="grid g2">{docs}</div></div></section>' if docs else ''}
{f'<section class="sec" id="files"><div class="wrap"><div class="sec-h"><div><h2>الملفات</h2></div></div><div class="grid g3">{files}</div></div></section>' if files else ''}
{cps_html(p)}
{f'<section class="sec" id="cert"><div class="wrap"><div class="sec-h"><div><h2>الشهادة</h2></div></div><a href="{pre}{p["certificate"]}" data-title="الشهادة"><img src="{pre}{p["certificate"]}" alt="الشهادة" style="width:100%;max-width:820px;border-radius:16px;box-shadow:0 14px 30px rgba(0,0,0,.12)"></a></div></section>' if p.get('certificate') else ''}
</div>
<script type="application/json" id="udata">{json.dumps(data, ensure_ascii=False).replace('</', '<\\/')}</script>
<script>{PLAYER_JS}</script>"""
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

# ---------- صفحة الاختبارات الموحدة ----------
TESTS_JS = r"""
const T=JSON.parse(document.getElementById('tdata').textContent);
const $=s=>document.querySelector(s);
function shuffle(q){const idx=q.o.map((_,i)=>i);for(let i=idx.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[idx[i],idx[j]]=[idx[j],idx[i]];}return {q:q.q,o:idx.map(i=>q.o[i]),a:idx.indexOf(q.a)};}
function openTest(pk,ti){
  const t=T[pk].tests[ti];const qs=t.shuffle?t.qs.map(shuffle):t.qs;const N=qs.length;const sel={};let sent=false;
  const box=$('#tp');box.innerHTML='<div class="card"><span class="kicker">'+T[pk].name+'</span><h2 style="font-size:32px;margin:6px 0">'+t.title+'</h2><p class="cp-tip">'+N+' أسئلة · اختر وغيّر كما تشاء، ثم «أرسل الإجابات». النجاح 80%.</p>'+qs.map((q,qi)=>'<div class="qz" data-q="'+qi+'"><b>'+(qi+1)+'. '+q.q+'</b><div class="qo">'+q.o.map((o,oi)=>'<button type="button" data-i="'+oi+'">'+o+'</button>').join('')+'</div></div>').join('')+'<div class="qbar"><button type="button" class="btn p" id="qsend" disabled>أرسل الإجابات (0 من '+N+')</button><button type="button" class="btn s" id="qr" style="display:none">أعد المحاولة</button><button type="button" class="btn s" id="qkey">🔑 مفتاح الإجابات</button></div><p class="qs" id="qs"></p></div>';
  const send=$('#qsend');
  box.querySelectorAll('.qz').forEach(z=>z.querySelectorAll('.qo button').forEach(b=>b.onclick=()=>{if(sent)return;sel[+z.dataset.q]=+b.dataset.i;z.querySelectorAll('.qo button').forEach(x=>x.classList.toggle('sel',x===b));const n=Object.keys(sel).length;send.textContent='أرسل الإجابات ('+n+' من '+N+')';send.disabled=n<N;}));
  function lock(showSel){sent=true;let ok=0;qs.forEach((q,qi)=>{const bs=box.querySelectorAll('.qz[data-q="'+qi+'"] .qo button');bs.forEach(x=>{x.classList.remove('sel');x.disabled=true;});if(showSel&&sel[qi]!==q.a)bs[sel[qi]].classList.add('no');if(sel[qi]===q.a)ok++;bs[q.a].classList.add('ok');});return ok;}
  send.onclick=()=>{const ok=lock(true);const pct=Math.round(ok/N*100);$('#qs').innerHTML=(pct>=80?'✅ ناجح: ':'⏳ لم تبلغ 80%: ')+ok+' من '+N+' ('+pct+'%)';send.style.display='none';$('#qkey').style.display='none';$('#qr').style.display='';};
  $('#qkey').onclick=()=>{lock(false);$('#qs').textContent='🔑 الإجابات الصحيحة مظللة بالأخضر (للمدرب).';send.style.display='none';$('#qkey').style.display='none';$('#qr').style.display='';};
  $('#qr').onclick=()=>openTest(pk,ti);
  box.scrollIntoView({behavior:'smooth',block:'start'});
}
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{const [pk,ti]=b.dataset.t.split(':');openTest(pk,+ti);});
"""

def build_tests():
    old = json.load(open('/tmp/oldq.json', encoding='utf-8')) if os.path.exists('/tmp/oldq.json') else None
    if old is None:
        import subprocess
        src = open(os.path.join(ROOT, 'training/questions.js'), encoding='utf-8').read()
        names = re.findall(r'^const ([A-Za-z_]+)', src, flags=re.M)
        out = subprocess.run(['node', '-e', f"const src=require('fs').readFileSync('{os.path.join(ROOT,'training/questions.js')}','utf8');const r=new Function(src+';return {{{','.join(names)}}}')();console.log(JSON.stringify(r))"], capture_output=True, text=True).stdout
        old = json.loads(out)
    Q, QZ = old['Q'], old['QUIZZES']
    def oldtest(key): return [{'q': Q[i]['q'], 'o': Q[i]['o'], 'a': 0} for i in QZ[key]['ids']]
    data = {}
    cards = ''
    for p in sorted(D['packages'], key=lambda x: x['slug'] != 'free'):
        tests = []
        if p['slug'] == 'free': tests.append({'title': 'الاختبار القبلي', 'sub': 'قبل أن تبدأ الوحدات', 'badge': 'قبل', 'qs': oldtest('pre'), 'shuffle': True})
        for u in p['units']:
            if u.get('quiz'): tests.append({'title': f'امتحان الوحدة {u["n"]}', 'sub': u['title'], 'badge': str(u['n']), 'qs': parse_quiz(u['quiz']), 'shuffle': False})
        if p['slug'] == 'free': tests.append({'title': 'الاختبار البعدي', 'sub': 'بعد إتمام الوحدات الخمس', 'badge': 'بعد', 'qs': oldtest('post'), 'shuffle': True})
        data[p['slug']] = {'name': p['name'], 'tests': tests}
        items = ''.join(f'<button type="button" class="tst" data-t="{p["slug"]}:{i}"><span class="num">{E(t["badge"])}</span><span><b>{E(t["title"])}</b><small>{len(t["qs"])} أسئلة · {E(t["sub"])}</small></span></button>' for i, t in enumerate(tests))
        cards += f'<section class="sec"{theme(p)}><div class="wrap"><div class="sec-h"><div><h2>{E(p["name"])}</h2><p>{len(tests)} اختبارات</p></div></div><div class="tlist">{items}</div></div></section>'
    body = f"""<section class="hero" style="padding-bottom:10px"><div class="wrap"><p class="crumb" style="margin-top:0"><a href="../workshop.html">الورشة</a> ← الاختبارات</p><span class="kicker">لكل حقيبة</span><h1>الاختبارات</h1><p class="lead">كل اختبارات الحقائب في مكان واحد، بالنسخة المعتمدة نفسها التي في منصة CPS. اختر اختبارًا، أو اعرض مفتاح إجاباته.</p></div></section>
{cards}
<section class="sec"><div class="wrap" id="tp"></div></section>
<style>
.tlist{{display:grid;gap:10px}}
.tst{{display:flex;flex-direction:row;gap:14px;align-items:center;text-align:right;font:inherit;background:#fff;border:1px solid #F1EADB;border-radius:18px;padding:12px 16px;cursor:pointer;box-shadow:0 6px 14px rgba(31,42,55,.05)}}
.tst:hover{{border-color:var(--a)}}
.tst .num{{width:48px;height:48px;flex:0 0 48px;border-radius:14px;display:grid;place-items:center;color:#fff;font-weight:700;font-size:19px;background:linear-gradient(150deg,var(--a),var(--b));box-shadow:inset 0 2px 0 rgba(255,255,255,.4),0 6px 12px rgba(0,0,0,.15)}}
.tst b{{display:block;font-size:22px;color:var(--b)}}.tst small{{color:var(--mute);font-size:17px}}
</style>
<script type="application/json" id="tdata">{json.dumps(data, ensure_ascii=False).replace('</', '<\\/')}</script>
<script>{TESTS_JS}</script>"""
    write('training/index.html', page('الاختبارات · الورشة', body, '../', 'workshop', '\n<meta name="robots" content="noindex">'))

# ---------- الكراسات التفاعلية ----------
WB_JS = r"""
const W=JSON.parse(document.getElementById('wbdata').textContent);
const KEY='masar-wb-'+W.slug;let S={};try{S=JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}};
const esc=t=>String(t==null?'':t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function field(f){
  const lab=f.label?'<label class="wl">'+esc(f.label)+(f.hint?' <span>'+esc(f.hint)+'</span>':'')+'</label>':'';
  let exl=(f.ex&&f.ex.length)?f.ex.slice():[];if(!exl.length&&typeof f.sample==='string'&&!f.from)exl=[f.sample];f._ex=exl;
  let exb=exl.length?'<button type="button" class="exb" data-ex="'+f.id+'">💡 أمثلة</button><div class="exs" id="ex-'+f.id+'" hidden>'+exl.map((e,i)=>'<button type="button" data-f="'+f.id+'" data-i="'+i+'">'+esc(e)+'</button>').join('')+'</div>':'';
  if(f.compose) exb='<button type="button" class="exb" data-compose="'+f.id+'">✨ ركّب من إجاباتك</button>'+exb;
  if(f.from) exb='<button type="button" class="exb" data-from="'+f.id+'">↩ انقل من الأوراق السابقة</button>'+exb;
  if(f.type==='text') return '<div class="wf">'+lab+'<div class="wr"><input type="text" data-id="'+f.id+'" value="'+esc(S[f.id])+'">'+exb+'</div></div>';
  if(f.type==='area') return '<div class="wf">'+lab+'<div class="wr"><textarea rows="3" data-id="'+f.id+'">'+esc(S[f.id])+'</textarea>'+exb+'</div></div>';
  if(f.type==='choice'||f.type==='multi'){const v=S[f.id]||(f.type==='multi'?[]:'');return '<div class="wf">'+lab+'<div class="chs" data-id="'+f.id+'" data-multi="'+(f.type==='multi'?1:0)+'">'+f.options.map(o=>'<button type="button" class="'+((f.type==='multi'?v.includes(o):v===o)?'on':'')+'">'+esc(o)+'</button>').join('')+'</div></div>';}
  if(f.type==='checks'){const v=S[f.id]||[];return '<div class="wf"><div class="cks" data-id="'+f.id+'">'+f.options.map((o,i)=>'<label><input type="checkbox" data-i="'+i+'" '+(v.includes(i)?'checked':'')+'> '+esc(o)+'</label>').join('')+'</div></div>';}
  if(f.type==='yesno'){const v=S[f.id]||[];return '<div class="wf"><table class="wt"><tr><th>السؤال</th><th>نعم</th><th>لا</th></tr>'+f.rows.map((r,i)=>'<tr><td>'+esc(r)+'</td>'+['نعم','لا'].map(a=>'<td><input type="radio" name="'+f.id+i+'" data-id="'+f.id+'" data-i="'+i+'" value="'+a+'" '+(v[i]===a?'checked':'')+'></td>').join('')+'</tr>').join('')+'</table></div>';}
  if(f.type==='table'){const v=S[f.id]||[];return '<div class="wf">'+(f.sample?'<button type="button" class="exb" data-tsample="'+f.id+'" style="margin-bottom:6px">💡 املأ بالمثال</button>':'')+'<div class="tw"><table class="wt"><tr><th>#</th>'+f.cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr>'+Array.from({length:f.rows},(_,r)=>'<tr><td>'+(r+1)+'</td>'+f.cols.map((c,ci)=>'<td><textarea rows="2" data-id="'+f.id+'" data-r="'+r+'" data-c="'+ci+'">'+esc((v[r]||[])[ci])+'</textarea></td>').join('')+'</tr>').join('')+'</table></div></div>';}
  if(f.type==='score'){const v=S[f.id]||{imp:[],a:[],b:[]};const opt=(k,r,vals)=>'<select data-id="'+f.id+'" data-k="'+k+'" data-r="'+r+'"><option value=""></option>'+vals.map(x=>'<option '+(String(v[k][r])===String(x)?'selected':'')+'>'+x+'</option>').join('')+'</select>';
    const sum=k=>v[k].reduce((a,b)=>a+(+b||0),0);
    return '<div class="wf"><div class="tw"><table class="wt"><tr><th>المعيار</th><th>الأهمية</th><th>درجة (أ)</th><th>درجة (ب)</th></tr>'+f.rows.map((r,i)=>'<tr><td>'+esc(r)+'</td><td>'+opt('imp',i,['عالية','متوسطة'])+'</td><td>'+opt('a',i,[1,2,3,4,5])+'</td><td>'+opt('b',i,[1,2,3,4,5])+'</td></tr>').join('')+'<tr class="sum"><td>المجموع</td><td></td><td>'+sum('a')+'</td><td>'+sum('b')+'</td></tr></table></div></div>';}
  return '';
}
function render(){
  document.getElementById('wb').innerHTML=W.sheets.map(sh=>'<section class="card ws" id="s'+sh.n+'"><span class="kicker">'+esc(sh.unit)+'</span><h2>الورقة '+sh.n+' · '+esc(sh.title)+'</h2>'+sh.groups.map(g=>'<div class="wg"><h3>'+esc(g.title)+'</h3>'+g.fields.map(field).join('')+'</div>').join('')+'</section>').join('');
  bind();
}
function bind(){
  const root=document.getElementById('wb');
  root.querySelectorAll('input[type=text][data-id],textarea[data-id]:not([data-r])').forEach(el=>el.oninput=()=>{S[el.dataset.id]=el.value;save();});
  root.querySelectorAll('textarea[data-r]').forEach(el=>el.oninput=()=>{const id=el.dataset.id;S[id]=S[id]||[];S[id][+el.dataset.r]=S[id][+el.dataset.r]||[];S[id][+el.dataset.r][+el.dataset.c]=el.value;save();});
  root.querySelectorAll('.chs').forEach(g=>g.querySelectorAll('button').forEach(b=>b.onclick=()=>{const id=g.dataset.id,val=b.textContent;if(g.dataset.multi==='1'){S[id]=S[id]||[];const k=S[id].indexOf(val);k<0?S[id].push(val):S[id].splice(k,1);b.classList.toggle('on');}else{S[id]=val;g.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));}save();}));
  root.querySelectorAll('.cks input').forEach(c=>c.onchange=()=>{const id=c.closest('.cks').dataset.id;S[id]=[...c.closest('.cks').querySelectorAll('input')].map((x,i)=>x.checked?i:-1).filter(i=>i>=0);save();});
  root.querySelectorAll('input[type=radio]').forEach(r=>r.onchange=()=>{const id=r.dataset.id;S[id]=S[id]||[];S[id][+r.dataset.i]=r.value;save();});
  root.querySelectorAll('select[data-id]').forEach(sl=>sl.onchange=()=>{const id=sl.dataset.id;S[id]=S[id]||{imp:[],a:[],b:[]};S[id][sl.dataset.k][+sl.dataset.r]=sl.value;save();render();});
  root.querySelectorAll('.exb').forEach(b=>b.onclick=()=>{const box=document.getElementById('ex-'+b.dataset.ex);box.hidden=!box.hidden;});
  root.querySelectorAll('.exs button').forEach(b=>b.onclick=()=>{const f=findF(b.dataset.f);S[f.id]=f._ex[+b.dataset.i];save();render();});
  root.querySelectorAll('[data-tsample]').forEach(b=>b.onclick=()=>{const f=findF(b.dataset.tsample);S[f.id]=JSON.parse(JSON.stringify(f.sample));save();render();});
  root.querySelectorAll('[data-from]').forEach(b=>b.onclick=()=>{const f=findF(b.dataset.from);const v=S[f.from];if(v){S[f.id]=v;save();render();}else alert('عبّئ الخانة الأصلية في الورقة السابقة أولًا');});
  root.querySelectorAll('[data-compose]').forEach(b=>b.onclick=()=>{const f=findF(b.dataset.compose);const v=k=>(S[k]||'').trim();let t=f.compose.replace(/\{(\w+)\}/g,(m,k)=>v(k)||'('+k+')');S[f.id]=t;save();render();});
}
function findF(id){for(const sh of W.sheets)for(const g of sh.groups)for(const f of g.fields)if(f.id===id)return f;}
document.getElementById('wsample').onclick=()=>{S={};for(const sh of W.sheets)for(const g of sh.groups)for(const f of g.fields)if(f.sample!==undefined)S[f.id]=JSON.parse(JSON.stringify(f.sample));save();render();};
document.getElementById('wclear').onclick=()=>{if(confirm('امسح كل ما في الكراسة؟')){S={};save();render();}};
document.getElementById('wprint').onclick=()=>window.print();
render();
"""

def build_workbooks():
    tiles = ''
    for slug in ('free', 'video'):
        path = os.path.join(ROOT, f'data/workbooks/{slug}.json')
        if not os.path.exists(path): continue
        W = json.load(open(path, encoding='utf-8'))
        p = next(x for x in D['packages'] if x['slug'] == slug)
        nav = ''.join(f'<a href="#s{sh["n"]}">{sh["n"]}. {E(sh["title"])}</a>' for sh in W['sheets'])
        body = f"""<div{theme(p)}>
<section class="phero" style="padding:26px 0 16px"><div class="wrap"><p class="crumb" style="margin-top:0"><a href="../workshop.html">الورشة</a> ← <a href="{slug}.html">{E(p["name"])}</a> ← {E(W["title"])}</p>
<span class="kicker">{E(p["name"])}</span><h1 style="font-size:40px">{E(W["title"])}</h1>
<p class="lead" style="margin:6px 0 0">اكتب في الخانات، أو اضغط «💡 أمثلة» بجانب أي خانة لتختار إجابة جاهزة. والنموذج المحلول يعبئ الكراسة كلها بمثال واحد متكامل: <b>{E(W["example"])}</b>.</p>
<div class="row" style="margin-top:14px"><button type="button" class="btn p" id="wsample">📋 النموذج المحلول</button><button type="button" class="btn s" id="wclear">↺ امسح وابدأ من جديد</button><button type="button" class="btn s" id="wprint">🖨 اطبع أو احفظ PDF</button></div></div></section>
<div class="tabs"><div class="wrap">{nav}</div></div>
<section class="sec"><div class="wrap" id="wb" style="display:grid;grid-template-columns:minmax(0,1fr);gap:20px"></div></section></div>
<style>
.ws{{min-width:0}}.ws h2{{font-size:30px;margin:4px 0 10px}}.wg{{margin-top:14px}}.wg h3{{font-size:23px;color:var(--a);margin:0 0 8px}}
.wf{{margin:0 0 12px}}.wl{{display:block;font-weight:700;color:var(--b);margin-bottom:4px}}.wl span{{font-weight:400;color:var(--mute);font-size:16px}}
.wr{{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-start}}.wr input,.wr textarea{{flex:1}}
.ws input[type=text],.ws textarea,.ws select{{font:inherit;font-size:19px;width:100%;border:1.5px solid var(--line);border-radius:12px;padding:8px 12px;background:#FFFEFA;text-align:right;direction:rtl}}
.ws textarea{{resize:vertical}}
.exb{{font:inherit;font-size:16px;font-weight:700;white-space:nowrap;border:0;border-radius:10px;padding:8px 12px;background:var(--soft);color:var(--b);cursor:pointer}}
.exs{{display:flex;flex-wrap:wrap;gap:6px;margin-top:2px;flex-basis:100%}}.exs[hidden]{{display:none}}.exs button{{font:inherit;font-size:16px;border:1.5px dashed var(--a);border-radius:10px;padding:4px 10px;background:#fff;cursor:pointer;color:var(--b)}}
.chs{{display:flex;flex-wrap:wrap;gap:8px}}.chs button{{font:inherit;font-size:18px;border:2px solid var(--line);border-radius:12px;padding:6px 14px;background:#fff;cursor:pointer}}.chs button.on{{border-color:var(--a);background:var(--soft);font-weight:700}}
.cks{{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}}.cks label{{display:flex;gap:8px;align-items:center}}
.tw{{overflow-x:auto}}.wt{{width:100%;border-collapse:collapse}}.wt th,.wt td{{border:1px solid var(--line);padding:6px;text-align:right;vertical-align:top}}.wt th{{background:var(--b);color:#fff;font-size:17px}}.wt td textarea{{font-size:17px;min-width:140px}}.wt tr.sum td{{font-weight:700;background:var(--soft)}}
@media (max-width:620px){{.cks{{grid-template-columns:1fr}}.wr{{flex-direction:column}}}}
@media print{{.bar,.tabs,.row,.crumb,.exb,.exs,footer.ft{{display:none!important}}.ws{{break-inside:avoid;box-shadow:none}}body{{background:#fff}}}}
</style>
<script type="application/json" id="wbdata">{json.dumps(W, ensure_ascii=False).replace('</', '<\\/')}</script>
<script>{WB_JS}</script>"""
        write(f'workshop/{slug}-workbook.html', page(f'{W["title"]} · {p["name"]}', body, '../', 'workshop', '\n<meta name="robots" content="noindex">'))

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
    build_method(); build_tool(); build_tests(); build_workbooks(); redirects()
    for p in PUB:
        st = load_status(p)
        if st and not gate_report(st)[2][3]: print(f'⚠ {p["name"]}: معروضة للجمهور ولم تعبر البوابة ج (الإطلاق) بعد')
