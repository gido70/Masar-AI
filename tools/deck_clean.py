import re
AR=re.compile(r'[\u0600-\u06FF]')
def clean(t):
    if '<span' in t: core=t
    else: core=t
    core=core.replace('«','').replace('»','')
    core=core.replace('، و',' و').replace('، ',' و')
    core=re.sub(r'[.؟!…:]+\s*$','',core.strip())
    return core
WARN=[]
def check(t,where=''):
    plain=re.sub(r'<[^>]+>','',t)
    if AR.search(plain) and (re.search(r'\d',plain) or ':' in plain or '–' in plain or '·' in plain) and not plain.strip().startswith('['):
        WARN.append((where,plain))
