#!/usr/bin/env python3
"""Phase 3 verification for the glossed artifact."""
import pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[3]
import re, sys, os, json, subprocess
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terms import TERMS, NEGATIVE_LOOKAHEAD

MD  = str(_ROOT/"docs/papers/deceptive-grounding-measurable-without-judge-eli5.md")
DOC = str(_ROOT/"docs/papers/deceptive-grounding-measurable-without-judge-eli5-glossed.html")
raw = open(DOC).read()
fails, notes = [], []
def ck(ok, msg):
    print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok: fails.append(msg)

# ---------------------------------------------------------------- 1. glossable source text
lines = open(MD).read().split("\n")
prose, i, n, fence, pic = [], 0, len(lines), False, False
while i < n:
    ln = lines[i]; s = ln.strip()
    if s.startswith("## 10. References"): break
    if s.startswith("```"): fence = not fence; i += 1; continue
    if fence: i += 1; continue
    if s.startswith("<picture"): pic = True
    if pic:
        if "</picture>" in s: pic = False
        i += 1; continue
    if re.match(r"^#{1,6} ", s) or s.startswith("|") or s == "---" or not s: i += 1; continue
    if s.startswith(">"):
        if i < 12 or "**Figure " in s:  i += 1; continue   # header block, figure captions
    prose.append(s); i += 1
PROSE = "\n".join(prose)
PROSE_NOMATH = re.sub(r"\$([^$\n]+)\$",
    lambda m: " " if re.match(r"^[\\A-Za-z(]", m.group(1)) and "**" not in m.group(1) else m.group(0),
    PROSE)

def src_count(pats, cs):
    tot = 0
    for p in pats:
        tail = NEGATIVE_LOOKAHEAD.get(p.lower(), "")
        tot += len(re.findall(r"(?<![\w-])" + re.escape(p) + tail + r"(?![\w-])",
                              PROSE_NOMATH, 0 if cs else re.I))
    return tot

# longest-match-first also applies to the source tally: a shorter pattern must not
# be counted where a longer approved one consumed the text.
COMPILED = []
for tid, disp, exp, pats, cs in TERMS:
    for p in pats:
        tail = NEGATIVE_LOOKAHEAD.get(p.lower(), "")
        COMPILED.append((len(p), re.compile(r"(?<![\w-])" + re.escape(p) + tail + r"(?![\w-])",
                                            0 if cs else re.I), tid))
COMPILED.sort(key=lambda r: -r[0])
expected = {}
i = 0
while i < len(PROSE_NOMATH):
    for _, rx, tid in COMPILED:
        m = rx.match(PROSE_NOMATH, i)
        if m:
            expected[tid] = expected.get(tid, 0) + 1; i = m.end(); break
    else:
        i += 1

# ---------------------------------------------------------------- 2. parse output
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.stack=[]; s.btn=[]; s.cur=None; s.sec="(preamble)"; s.p={}; s.text=[]
        s.badctx=[]; s.figs=[]; s.opens=[]; s.void={"br","img","source","hr","meta","link","input"}
        s.nest=0; s.nestbad=0
    def handle_starttag(s, tag, attrs):
        a=dict(attrs)
        if tag not in s.void:
            s.stack.append((tag,a)); s.opens.append(tag)
        if tag=="button" and "gloss-term" in a.get("class",""):
            if s.nest: s.nestbad+=1
            s.nest+=1
            s.cur=a.get("data-term-id"); s.btn.append(s.cur)
            ctx={t for t,_ in s.stack[:-1]}
            cls=" ".join(x.get("class","") for _,x in s.stack)
            if ctx & {"h1","h2","h3","h4","h5","h6","figcaption","table","pre","math"} or "math" in cls.split():
                s.badctx.append(s.cur)
        if tag in ("h1","h2","h3","h4","h5","h6"): s.sec=None; s.pending=tag
        if tag=="p": s.p[s.sec]=s.p.get(s.sec,0)+1
        if tag=="figure" and "paper-figure" in a.get("class",""): s.figs.append(a)
        if tag=="img" and any(t=="figure" for t,_ in s.stack): s.figs[-1]["_img"]=a
    def handle_endtag(s, tag):
        if getattr(s,"pending",None)==tag: s.pending=None; s.sec=(s.sec or "").strip()
        if tag=="button" and s.nest: s.nest-=1
        for k in range(len(s.stack)-1,-1,-1):
            if s.stack[k][0]==tag: del s.stack[k:]; break
        if s.opens and tag in s.opens: s.opens.remove(tag)
    def handle_data(s, d):
        if getattr(s,"pending",None) and s.stack and s.stack[-1][0]==s.pending:
            s.sec=(s.sec or "")+d
        if any(t in ("script","style") for t,_ in s.stack): return
        ids={x.get("id","") for _,x in s.stack}
        cls=" ".join(x.get("class","") for _,x in s.stack)
        if "references" in ids or "doc-header" in cls: return
        s.text.append((d, {t for t,_ in s.stack}, cls))
p=P(); p.feed(raw)

got={}
for b in p.btn: got[b]=got.get(b,0)+1

print("\n=== 1. Occurrence coverage (source prose vs .gloss-term buttons) ===")
bad=[(t,expected.get(t,0),got.get(t,0)) for t in {*expected,*got} if expected.get(t,0)!=got.get(t,0)]
for t,e,g in sorted(bad): print(f"    {t:22s} expected={e} got={g}")
ck(not bad, f"all {len(TERMS)} terms match ({sum(got.values())} buttons total)")

print("\n=== 2. No bare occurrences outside .gloss-term (math exempt) ===")
bare=[]
for d, ctx, cls in p.text:
    if ctx & {"button"}: continue
    if "math" in cls.split() or "math" in ctx: continue
    if ctx & {"h1","h2","h3","h4","h5","h6","figcaption","table","pre","title"}: continue
    for _,rx,tid in COMPILED:
        for m in rx.finditer(d):
            bare.append((tid, m.group(0), d[max(0,m.start()-30):m.end()+30]))
for t,w,c in bare[:12]: print(f"    {t}: {w!r} … {c.strip()[:80]!r}")
ck(not bare, f"zero bare occurrences ({len(bare)} found)")

print("\n=== 2b. Cross-element bare occurrences (term split by a tag boundary) ===")
# A term whose text is broken by </strong> etc. is invisible to a per-text-node scan
# (that blindness is what let one bare "clean trials" through and made the expected
# count skip it too). Rebuild each block's visible text and re-scan.
# scan only the wrappable region: after </header>, before <section id="references">
_region = raw[raw.index("</header>"):raw.index('<section id="references">')]
blocks = re.findall(r"<(?:p|li|dd|blockquote)\b[^>]*>(.*?)</(?:p|li|dd|blockquote)>", _region, re.S)
split_hits = []
for b in blocks:
    if 'id="references"' in b: continue
    plain = re.sub(r"<[^>]+>", "", b)
    plain = plain.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").replace("&#36;","$")
    stripped = re.sub(r"<button[^>]*class=\"gloss-term\"[^>]*>.*?</button>", "\x00", b, flags=re.S)
    stripped = re.sub(r"<span class=\"math[^\"]*\">.*?</span>", "\x00", stripped, flags=re.S)
    stripped = re.sub(r"<[^>]+>", "", stripped)
    stripped = stripped.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">")
    for _, rx, tid in COMPILED:
        for m in rx.finditer(stripped):
            split_hits.append((tid, m.group(0), stripped[max(0,m.start()-35):m.end()+25].strip()))
# Declared carve-out. `**80/80 clean** trials` splits the term across a </strong>;
# HTML tags cannot overlap, so wrapping it would mean moving the source's emphasis,
# which this rewrite may not do. Declared here so any NEW split fails the gate.
DECLARED_SPLIT = {("clean-trial", "clean trials")}
undeclared = [h for h in split_hits if (h[0], h[1]) not in DECLARED_SPLIT]
for t,w,c in split_hits: print(f"    {'declared' if (t,w) in DECLARED_SPLIT else 'UNDECLARED'}  {t}: {w!r} … {c[:70]!r}")
ck(not undeclared, f"every cross-element bare occurrence is declared ({len(split_hits)} total, {len(undeclared)} undeclared)")

print("\n=== 3. Overlap / nesting ===")
ck(p.nestbad==0, f"zero nested .gloss-term ({p.nestbad})")

print("\n=== 4. Dictionary symmetry ===")
G=json.loads(re.search(r"const GLOSS_TERMS = (\{.*?\n\});", raw, re.S).group(1))
ck(set(got)<=set(G), "every data-term-id resolves to a GLOSS_TERMS key")
ck(set(G)==set(got), f"every dictionary entry used in body (unused: {sorted(set(G)-set(got))})")
ck(len(G)==len(TERMS), f"dictionary holds all {len(TERMS)} approved terms ({len(G)})")

print("\n=== 5. Non-prose passthrough ===")
ck(not p.badctx, f"zero .gloss-term in heading/math/table/figcaption/pre ({p.badctx[:5]})")
_a=raw.index('<section id="references">'); refs = raw[_a:raw.index("</section>", _a)]
ck("gloss-term" not in refs, "references section carries zero .gloss-term")
hdr = raw[raw.index('<header class="doc-header">'):raw.index("</header>")]
ck("gloss-term" not in hdr, "doc-header carries zero .gloss-term")

print("\n=== 6. Structure fidelity (<p> per section) ===")
_r=subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),"check6.py")],
                  capture_output=True, text=True)
print("   ", _r.stdout.strip().replace("\n","\n    "))
ck(_r.returncode==0, "per-section <p> counts match md prose blocks")

print("\n=== 7. Named forms ===")
nf_md = open(MD).read().count("*Named form:*")
nf_html = raw.count('class="named-form"')
ck(nf_md==nf_html, f"named forms carried 1:1 (source {nf_md}, output {nf_html})")

print("\n=== 8. Math gate ===")
# Prefer the copy vendored into this repo so the gate runs for collaborators,
# in CI, and in cloud/web sessions; fall back to a globally-installed skill.
_CM = _ROOT/".claude/skills/paper-gloss/scripts/check_math.py"
if not _CM.exists():
    _CM = pathlib.Path(os.path.expanduser("~/.claude/skills/paper-gloss/scripts/check_math.py"))
ck(_CM.exists(), f"check_math.py resolvable ({_CM})")
r=subprocess.run([sys.executable, str(_CM), DOC], capture_output=True, text=True)
print("   ", (r.stdout+r.stderr).strip()[:600] or "(no output)")
ck(r.returncode==0, "check_math.py exits clean")
ck(raw.count('data-math-verbatim')==0, "zero Tier 3 verbatim fallbacks")

print("\n=== 9. Figures ===")
ck(len(p.figs)==3, f"3 paper-figure elements ({len(p.figs)})")
ck(raw.count('data:image/png;base64,')==6, f"6 inlined data URIs (light+dark x3): {raw.count('data:image/png;base64,')}")
ck(all(f.get("_img",{}).get("alt") for f in p.figs), "every figure has non-empty alt")
ck(raw.count("window.closeGlossPopover")==1 and raw.count("window.closeGlossPanel")==1
   and raw.count("window.closeFigureLightbox")==1 and raw.count("window.closeGlossSurfaces")==1,
   "all four window.close* hooks assigned")
ck(raw.count("id = 'figure-lightbox'")==1, "exactly one lightbox")

print("\n=== 10. Well-formedness ===")
ck(not p.opens, f"every tag closed (unclosed: {p.opens[:6]})")
for t in (r"<html[ >]", r"<head[ >]", r"<body[ >]", r"<title>"):
    ck(len(re.findall(t, raw))==1, f"exactly one {t}")
ck(raw.lower().startswith("<!doctype html>"), "doctype present")
ck(bool(re.search(r"<title>\S", raw)), "non-empty <title>")

print("\n=== 11. Self-containment ===")
for pat,label in [(r'src="https?://','external src'), (r'<link[^>]+href="https?://','external stylesheet'),
                  (r'@import','@import'), (r'url\(\s*["\']?https?://','css url()')]:
    c=len(re.findall(pat, raw)); ck(c==0, f"zero {label} ({c})")
ck(raw.count("data:image/png;base64,")>0, "data: URIs present and permitted")

print("\n=== 12. Theming completeness ===")
css=re.search(r"<style>(.*?)</style>", raw, re.S).group(1)
used={m.group(1) for m in re.finditer(r"var\((--[\w-]+)\)", css)}
blocks={"root":r":root\{(.*?)\}", "media":r"@media \(prefers-color-scheme:dark\)\{\s*:root\{(.*?)\}",
        "dark":r':root\[data-theme="dark"\]\{(.*?)\}', "light":r':root\[data-theme="light"\]\{(.*?)\}'}
defined={}
for k,rx in blocks.items():
    m=re.search(rx, css, re.S)
    defined[k]={x.group(1) for x in re.finditer(r"(--[\w-]+)\s*:", m.group(1))} if m else set()
palette = defined["dark"]
ck(used<=defined["root"], f"all vars defined in :root (missing: {sorted(used-defined['root'])})")
for k in ("media","dark","light"):
    ck(palette<=defined[k], f"palette redefined in {k} (missing: {sorted(palette-defined[k])})")

print("\n" + ("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILURES"))
sys.exit(1 if fails else 0)
