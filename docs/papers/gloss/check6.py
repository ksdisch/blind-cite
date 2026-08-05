#!/usr/bin/env python3
"""Structure fidelity: per-section <p> count vs md prose blocks.

md prose block  = a paragraph or a blockquote that is NOT a figure caption.
Excluded because they map to something other than <p>: headings, list items
(<li>), table rows (<table>), code fences (<pre>), <picture> blocks, and figure
captions (<figcaption>).  The leading header block maps into <header> together
with the title section's subtitle and lineage lines, so it is counted there.
"""
import pathlib
_ROOT = pathlib.Path(__file__).resolve().parents[3]
import re, sys
MD  = str(_ROOT/"docs/papers/deceptive-grounding-measurable-without-judge-eli5.md")
DOC = str(_ROOT/"docs/papers/deceptive-grounding-measurable-without-judge-eli5-glossed.html")

# ---- md side
md = open(MD).read().split("\n")
exp, sec, fence, pic = {}, None, False, False
for k, ln in enumerate(md):
    t = ln.strip()
    if t.startswith("```"): fence = not fence; continue
    if fence: continue
    if t.startswith("<picture"): pic = True
    if pic:
        if "</picture>" in t: pic = False
        continue
    h = re.match(r"^#{1,6}\s+(.*)$", t)
    if h: sec = h.group(1).strip(); exp.setdefault(sec, 0); continue
    if not t or t == "---" or t.startswith("|"): continue
    if re.match(r"^(-|\d+\.)\s", t): continue                 # list item -> <li>
    if t.startswith(">"):
        if k < 12: continue                                   # header block, counted below
        if "**Figure " in t: continue                         # -> <figcaption>
    exp[sec] = exp.get(sec, 0) + 1
title = next(iter(exp))
exp[title] += 1        # the header block's note joins subtitle+lineage in <header>

# ---- html side
raw = open(DOC).read()
main = raw[raw.index("<main>"):raw.index("</main>")]
parts = re.split(r"<h[1-6][^>]*>(.*?)</h[1-6]>", main, flags=re.S)
got, cur = {}, title
got[cur] = len(re.findall(r"<p[ >]", parts[0]))                                # <header> block
for j in range(1, len(parts), 2):
    name = re.sub(r"<[^>]+>", "", parts[j])
    name = name.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">").strip()
    got[name] = got.get(name, 0) + len(re.findall(r"<p[ >]", parts[j+1]))

bad = [(k, v, got.get(k, 0)) for k, v in exp.items() if v != got.get(k, 0)]
for k, e, g in bad: print(f"  MISMATCH  {k[:60]:60s} md={e} html={g}")
print(f"  sections: md={len(exp)} html={len(got)} | total <p>: md={sum(exp.values())} html={sum(got.values())}")
print("  PASS" if not bad else f"  FAIL ({len(bad)})")
sys.exit(1 if bad else 0)
