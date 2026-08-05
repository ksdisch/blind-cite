import pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[3]

#!/usr/bin/env python3
"""Build the glossed HTML artifact from the paper-eli5 markdown, 1:1."""
import re, sys, base64, os, json, html as _html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terms import TERMS, NEGATIVE_LOOKAHEAD

SRC = str(_ROOT/"docs/papers/deceptive-grounding-measurable-without-judge-eli5.md")
FIGDIR = str(_ROOT/"docs/paper")
OUT = str(_ROOT/"docs/papers/deceptive-grounding-measurable-without-judge-eli5-glossed.html")

# ---------------------------------------------------------------- term matching
COMPILED = []
for tid, disp, exp, pats, cs in TERMS:
    for p in pats:
        tail = NEGATIVE_LOOKAHEAD.get(p.lower(), "")
        rx = r"(?<![\w-])" + re.escape(p) + tail + r"(?![\w-])"
        COMPILED.append((len(p), re.compile(rx, 0 if cs else re.I), tid))
COMPILED.sort(key=lambda r: -r[0])          # longest-match-first, no overlap

def apply_terms(text):
    res, i, n = [], 0, len(text)
    while i < n:
        hit = None
        for _, rx, tid in COMPILED:
            m = rx.match(text, i)
            if m:
                hit = (m, tid); break
        if hit:
            m, tid = hit
            res.append('<button type="button" class="gloss-term" data-term-id="%s">%s</button>'
                       % (tid, m.group(0)))
            i = m.end()
        else:
            res.append(text[i]); i += 1
    return "".join(res)

NEVER_WRAP = {"h1","h2","h3","h4","h5","h6","figcaption","table","pre","math","button","script","style"}

def wrap_terms(frag):
    """Wrap approved terms in text nodes, never inside NEVER_WRAP or .math."""
    out, stack, excl_depth = [], [], 0
    for tok in re.split(r"(<[^>]+>)", frag):
        if tok.startswith("<") and tok.endswith(">"):
            m = re.match(r"</?\s*([a-zA-Z0-9]+)", tok)
            name = m.group(1).lower() if m else ""
            if tok.startswith("</"):
                if stack:
                    if stack.pop(): excl_depth -= 1
            elif not tok.endswith("/>") and name not in ("br","img","source","hr","meta","link"):
                excl = name in NEVER_WRAP or 'class="math' in tok
                stack.append(excl)
                if excl: excl_depth += 1
            out.append(tok)
        elif tok:
            out.append(tok if excl_depth else apply_terms(tok))
    return "".join(out)

# ---------------------------------------------------------------- math (Tier 1)
MACROS = {r"\cap":"∩", r"\cup":"∪", r"\geq":"≥", r"\leq":"≤", r"\times":"×",
          r"\in":"∈", r"\neq":"≠", r"\subset":"⊂", r"\approx":"≈", r"\cdot":"·"}
TIER1 = 0
def tier1(tex):
    """Convert an inline TeX expression to unicode + HTML (Tier 1)."""
    global TIER1
    TIER1 += 1
    out, i, n = [], 0, len(tex)
    while i < n:
        if tex.startswith(r"\text{", i):
            j = tex.index("}", i)
            out.append(esc(tex[i+6:j]))        # multi-letter names stay upright
            i = j + 1; continue
        mac = None
        for k, v in MACROS.items():
            if tex.startswith(k, i) and not re.match(r"[a-zA-Z]", tex[i+len(k):i+len(k)+1] or " "):
                mac = (k, v); break
        if mac:
            out.append(mac[1]); i += len(mac[0]); continue
        c = tex[i]
        if c.isalpha() and not (i and tex[i-1].isalpha()) and not tex[i+1:i+2].isalpha():
            out.append("<i>%s</i>" % c)        # single-letter variable -> italic
        elif c == "-":
            out.append("−")                     # U+2212, never a hyphen
        else:
            out.append(esc(c))
        i += 1
    body = "".join(out)
    cls = "math math-flow" if len(body) > 40 else "math"
    return '<span class="%s">%s</span>' % (cls, body)

# ---------------------------------------------------------------- inline markdown
def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def inline(s):
    holds = []
    def hold(h):
        holds.append(h); return "\x00%d\x00" % (len(holds)-1)
    s = re.sub(r"`([^`]+)`", lambda m: hold("<code>%s</code>" % esc(m.group(1))), s)
    # Currency guard: "$0.45 ceiling ... $0.10" would otherwise read as a math
    # span. Math bodies here start with a backslash, letter or paren and never
    # carry markdown emphasis; a digit-initial body is an amount, not notation.
    def maybe_math(m):
        b = m.group(1)
        if re.match(r"^[\\A-Za-z(]", b) and "**" not in b:
            return hold(tier1(b))
        return m.group(0)
    s = re.sub(r"\$([^$\n]+)\$", maybe_math, s)
    s = esc(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: holds[int(m.group(1))], s)
    return s

# ---------------------------------------------------------------- figures
def datauri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

# ---------------------------------------------------------------- parse + emit
lines = open(SRC).read().split("\n")
body, i, n = [], 0, len(lines)
sec_counts, cur_sec = {}, "(preamble)"
FIGS = 0

def addp(h):
    sec_counts[cur_sec] = sec_counts.get(cur_sec, 0) + h.count("<p")
    body.append(h)

# --- header block (the leading blockquote) + title block
hdr = []
while i < n and lines[i].startswith(">"):
    hdr.append(lines[i][1:].strip()); i += 1
meta = {}
for ln in hdr:
    m = re.match(r"\*\*(.+?):\*\*\s*(.*)", ln)
    if m: meta[m.group(1)] = m.group(2)
note = next((l for l in hdr if l.startswith("This mirrors")), "")
while i < n and (not lines[i].startswith("# ")): i += 1
title = lines[i][2:].strip(); i += 1
rest = []
while i < n and not lines[i].startswith("---"):
    if lines[i].strip(): rest.append(lines[i].strip())
    i += 1
i += 1

body.append('<header class="doc-header">')
body.append('  <div class="eyebrow">Plain-English rewrite</div>')
body.append("  <h1>%s</h1>" % inline(title))
body.append('  <p class="doc-subtitle">%s</p>' % inline(rest[0]))
body.append('  <p class="doc-lineage">%s</p>' % inline(rest[1]))
body.append('  <dl class="doc-meta">')
for k in ("Paper", "Source project", "Source file", "Generated"):
    if k in meta:
        body.append("    <dt>%s</dt><dd>%s</dd>" % (esc(k), inline(meta[k])))
body.append("  </dl>")
body.append('  <p class="doc-note">%s</p>' % inline(note))
body.append("</header>")
HDR_END = len(body)            # doc-header is metadata furniture, never term-wrapped:
                               # its "Paper" row restates the title, which would double-count.
sec_counts["(preamble)"] = 3   # subtitle, lineage, note

# --- main body
while i < n:
    ln = lines[i]
    s = ln.strip()

    if not s or s == "---":
        i += 1; continue

    m = re.match(r"^(#{1,6})\s+(.*)$", ln)
    if m:
        lvl, txt = len(m.group(1)), m.group(2)
        cur_sec = ln
        sec_counts.setdefault(cur_sec, 0)
        num = re.match(r"^(\d+(?:\.\d+)?)\.?\s+(.*)$", txt)
        if num:
            inner = '<span class="sec-num">%s</span> %s' % (num.group(1), inline(num.group(2)))
            # keep textContent byte-identical to the source heading
            inner = inner.replace('</span> ', '</span>%s' % (txt[len(num.group(1)):len(txt)-len(num.group(2))]), 1)
        else:
            inner = inline(txt)
        body.append("<h%d>%s</h%d>" % (lvl, inner, lvl))
        i += 1; continue

    if s.startswith("```"):
        i += 1; code = []
        while i < n and not lines[i].strip().startswith("```"):
            code.append(lines[i]); i += 1
        i += 1
        body.append('<div class="scroll-x"><pre class="code"><code>%s</code></pre></div>'
                    % esc("\n".join(code)))
        continue

    if s.startswith("<picture"):
        blk = []
        while i < n and "</picture>" not in lines[i]:
            blk.append(lines[i]); i += 1
        blk.append(lines[i]); i += 1
        joined = "\n".join(blk)
        dark = re.search(r'srcset="([^"]+)"', joined).group(1)
        light = re.search(r'src="([^"]+)"', joined).group(1)
        alt = re.search(r'alt="([^"]+)"', joined).group(1)
        while i < n and not lines[i].strip(): i += 1
        cap = lines[i][1:].strip(); i += 1
        FIGS += 1
        # id comes from the caption's own number, not document order: this paper
        # presents Figure 3 before Figure 2, so a counter mislabels both anchors.
        _cn = re.search(r"Figure (\d+)", cap)
        fid = "figure-%s" % (_cn.group(1) if _cn else FIGS)
        # Paired <img> rather than <picture>: <picture> keys off prefers-color-scheme
        # only, so a viewer toggling the artifact's theme on an opposite-scheme OS
        # would get a figure that fights the page. CSS below honours BOTH signals.
        body.append(
            '<figure class="paper-figure" id="%s">\n'
            '  <img class="fig-light" src="%s" alt="%s" loading="lazy">\n'
            '  <img class="fig-dark" src="%s" alt="%s" loading="lazy">\n'
            '  <figcaption>%s</figcaption>\n'
            '</figure>' % (fid, datauri(os.path.join(FIGDIR, os.path.basename(light))), esc(alt),
                           datauri(os.path.join(FIGDIR, os.path.basename(dark))), esc(alt),
                           inline(cap)))
        continue

    if s.startswith("|"):
        rows = []
        while i < n and lines[i].strip().startswith("|"):
            rows.append(lines[i].strip()); i += 1
        cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
        head, data = cells[0], cells[2:]
        h = ['<div class="scroll-x"><table>', "<thead><tr>"]
        h += ["<th>%s</th>" % inline(c) for c in head]
        h.append("</tr></thead><tbody>")
        for r in data:
            h.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
        h.append("</tbody></table></div>")
        body.append("".join(h))
        continue

    if s.startswith(">"):
        cls = "framing" if "Framing" in s or "framing" in s else "template-quote"
        addp('<blockquote class="%s"><p>%s</p></blockquote>' % (cls, inline(s[1:].strip())))
        i += 1; continue

    if re.match(r"^(-|\d+\.)\s", s):
        tag = "ul" if s.startswith("-") else "ol"
        items = []
        while i < n and re.match(r"^(-|\d+\.)\s", lines[i].strip()):
            items.append(re.sub(r"^(-|\d+\.)\s+", "", lines[i].strip())); i += 1
        body.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
        continue

    if s.startswith("*In plain words:"):
        inner = re.sub(r"^\*(.*)\*$", r"\1", s)
        inner = re.sub(r"^In plain words:\s*", "", inner)
        addp('<p class="plain-words"><em>In plain words:</em> %s</p>' % inline(inner))
        i += 1; continue

    addp("<p>%s</p>" % inline(s))
    i += 1

# The references section is in the never-wrap bucket: it legitimately contains
# `synthetic_Y`, `prior_completing`, `Cy`, `RAG-4` and `schema` as citation text.
_refs = next((k for k, b in enumerate(body) if b.startswith("<h2>") and "References" in b), len(body))
HTML_BODY = ("\n".join(body[:HDR_END]) + "\n"
             + wrap_terms("\n".join(body[HDR_END:_refs])) + "\n"
             + '<section id="references">\n' + "\n".join(body[_refs:]) + "\n</section>")

GLOSS = {tid: {"term": disp, "expansion": exp} for tid, disp, exp, _, _ in TERMS}
open(str(_ROOT/"docs/papers/gloss/.sec_counts.json"), "w").write(json.dumps(sec_counts, indent=1))
open(str(_ROOT/"docs/papers/gloss/.body.html"), "w").write(HTML_BODY)
open(str(_ROOT/"docs/papers/gloss/.gloss.json"), "w").write(json.dumps(GLOSS, ensure_ascii=False, indent=2))
print("figures:", FIGS, "| tier1 math spans:", TIER1, "| terms:", len(GLOSS))

from shell import CSS, JS
TITLE = "Deceptive grounding is measurable without a judge — and a null at N=20 did not survive a pre-registered extension to N=80"
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<style>{CSS}</style>
</head>
<body>
<button id="gloss-panel-toggle" aria-expanded="false" aria-controls="gloss-panel">📖 Glossary ({len(GLOSS)})</button>
<main>
{HTML_BODY}
</main>
<div id="gloss-popover" class="gloss-popover" role="tooltip" hidden>
  <button class="gloss-popover-close" aria-label="Close">&times;</button>
  <div class="gloss-popover-term"></div>
  <div class="gloss-popover-expansion"></div>
</div>
<div id="gloss-backdrop" class="gloss-backdrop" hidden></div>
<aside id="gloss-panel" class="gloss-panel" hidden aria-label="Glossary">
  <button class="gloss-panel-close" aria-label="Close">&times;</button>
  <h2>Glossary</h2>
  <div class="scroll-x"><table>
    <thead><tr><th>Term</th><th>Plain-English expansion</th></tr></thead>
    <tbody id="gloss-panel-rows"></tbody>
  </table></div>
</aside>
<script>
  const GLOSS_TERMS = {json.dumps(GLOSS, ensure_ascii=False, indent=2)};
</script>
<script>{JS}</script>
</body>
</html>
"""
open(OUT,"w").write(page)
print("wrote", OUT, f"({len(page)/1024/1024:.2f} MB)")
