"""نسخة مستقلة من الكراسة التفاعلية لمنصة CPS (29 أكتوبر 2026).
ملف HTML واحد بلا أي رابط أو صورة أو شعار أو خط من موقع مسار: البيانات والسكربت والتنسيق كلها داخل الملف، والخط من Google Fonts فقط.
يُرفع إلى مستودع lib-6931de باسم يصعب تخمينه، ويربطه زر الصفحة الأخيرة في كراسة CPS.
التشغيل: python3 tools/build_standalone_workbook.py <slug> "<عنوان الحقيبة بلا اسم المنصة>" <ملف الناتج>
"""
import json, sys, os, html, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug, label, out = sys.argv[1:4]
W = json.load(open(os.path.join(ROOT, f'data/workbooks/{slug}.json'), encoding='utf-8'))
W.pop('pkg', None)
src = open(os.path.join(ROOT, 'tools/build_site.py'), encoding='utf-8').read()
exec(re.search(r'(def wb_glossary.*?\nGLS_CSS = .*?\n)', src, re.S).group(1))
js = re.search(r'WB_JS = r"""(.*?)"""', src, re.S).group(1).replace("'masar-wb-'", "'wb-'")
E = html.escape
nav = ''.join(f'<a href="#s{sh["n"]}">{sh["n"]}. {E(sh["title"])}</a>' for sh in W['sheets'])
doc = f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{E(W['title'])} · {E(label)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--a:#B7791F;--b:#123E6B;--soft:#FBF4E4;--line:#E3DCCB;--mute:#5B6675;--bg:#FFFDF7}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:#1F2A37;font-family:Tajawal,Tahoma,'Segoe UI',Arial,sans-serif;font-size:18px;line-height:1.7}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 18px}}
header{{background:linear-gradient(180deg,#F7EEDB,#FFFDF7);padding:28px 0 16px;border-bottom:1px solid var(--line)}}
.kicker{{display:inline-block;background:var(--soft);color:var(--a);font-weight:700;font-size:15px;border-radius:999px;padding:2px 12px}}
h1{{font-size:36px;margin:8px 0 6px;color:var(--b)}}.lead{{margin:0;color:#334}}
.row{{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}}
.btn{{font:inherit;font-weight:700;font-size:17px;border-radius:12px;padding:9px 18px;cursor:pointer;border:2px solid var(--b)}}.btn.p{{background:var(--b);color:#fff}}.btn.s{{background:#fff;color:var(--b)}}
.tabs{{position:sticky;top:0;z-index:5;background:rgba(255,253,247,.96);border-bottom:1px solid var(--line)}}.tabs .wrap{{display:flex;flex-wrap:wrap;gap:8px;padding:10px 18px}}
.tabs a{{text-decoration:none;color:var(--b);font-weight:700;font-size:15px;border:1.5px solid var(--line);border-radius:999px;padding:4px 12px;background:#fff}}
main{{padding:22px 0 40px}}#wb{{display:grid;grid-template-columns:minmax(0,1fr);gap:20px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 4px 14px rgba(18,62,107,.06)}}
.ws{{min-width:0}}.ws h2{{font-size:28px;margin:4px 0 10px;color:var(--b)}}.wg{{margin-top:14px}}.wg h3{{font-size:22px;color:var(--a);margin:0 0 8px}}
.wf{{margin:0 0 12px}}.wl{{display:block;font-weight:700;color:var(--b);margin-bottom:4px}}.wl span{{font-weight:400;color:var(--mute);font-size:16px}}
.wr{{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-start}}.wr input,.wr textarea{{flex:1}}
.ws input[type=text],.ws textarea,.ws select{{font:inherit;font-size:18px;width:100%;border:1.5px solid var(--line);border-radius:12px;padding:8px 12px;background:#FFFEFA;text-align:right;direction:rtl}}
.ws textarea{{resize:vertical}}
.exb{{font:inherit;font-size:15px;font-weight:700;white-space:nowrap;border:0;border-radius:10px;padding:8px 12px;background:var(--soft);color:var(--b);cursor:pointer}}
.exs{{display:flex;flex-wrap:wrap;gap:6px;margin-top:2px;flex-basis:100%}}.exs[hidden]{{display:none}}.exs button{{font:inherit;font-size:15px;border:1.5px dashed var(--a);border-radius:10px;padding:4px 10px;background:#fff;cursor:pointer;color:var(--b)}}
.chs{{display:flex;flex-wrap:wrap;gap:8px}}.chs button{{font:inherit;font-size:17px;border:2px solid var(--line);border-radius:12px;padding:6px 14px;background:#fff;cursor:pointer}}.chs button.on{{border-color:var(--a);background:var(--soft);font-weight:700}}
.cks{{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}}.cks label{{display:flex;gap:8px;align-items:center}}
.tw{{overflow-x:auto}}.wt{{width:100%;border-collapse:collapse}}.wt th,.wt td{{border:1px solid var(--line);padding:6px;text-align:right;vertical-align:top}}.wt th{{background:var(--b);color:#fff;font-size:16px}}.wt td textarea{{font-size:16px;min-width:140px}}.wt tr.sum td{{font-weight:700;background:var(--soft)}}
@media (max-width:620px){{.cks{{grid-template-columns:1fr}}.wr{{flex-direction:column}}h1{{font-size:28px}}}}
{GLS_CSS}
@media print{{.tabs,.row,.exb,.exs{{display:none!important}}.ws{{break-inside:avoid;box-shadow:none}}body{{background:#fff}}}}
</style></head><body>
<header><div class="wrap"><span class="kicker">{E(label)}</span><h1>{E(W['title'])}</h1>
<p class="lead">اكتب في الخانات، أو اضغط «💡 أمثلة» بجانب أي خانة لتختار إجابة جاهزة. والنموذج المحلول يعبئ الكراسة كلها بمثال واحد متكامل: <b>{E(W['example'])}</b>. وحيث ترى «✨ ركّب من إجاباتك» يتكوّن برومبت جاهز، تنسخه بـ«📋 انسخ» وتلصقه في نموذج الذكاء الاصطناعي.</p>
<div class="row"><button type="button" class="btn p" id="wsample">📋 النموذج المحلول</button><button type="button" class="btn s" id="wclear">↺ امسح وابدأ من جديد</button><button type="button" class="btn s" id="wprint">🖨 اطبع أو احفظ PDF</button></div>{wb_glossary(W)}</div></header>
<nav class="tabs"><div class="wrap">{nav}</div></nav>
<main><div class="wrap" id="wb"></div></main>
<script type="application/json" id="wbdata">{json.dumps(W, ensure_ascii=False).replace('</', '<\\/')}</script>
<script>{js}</script></body></html>"""
open(out, 'w', encoding='utf-8').write(doc)
bad = [m for m in re.findall(r'(?:https?:)?//[^\s"\'<>)]+', doc) if 'fonts.g' not in m]
print('✓', out, f'{len(doc)//1024} KB', '· روابط خارجية غير الخط:', bad or 'لا شيء')
