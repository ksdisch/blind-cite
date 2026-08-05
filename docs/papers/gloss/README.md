# Glossed-artifact generator

Rebuilds `docs/papers/deceptive-grounding-measurable-without-judge-eli5-glossed.html`
from `docs/papers/deceptive-grounding-measurable-without-judge-eli5.md`, 1:1.
Committed for the same reason `docs/paper/figures.py` is: a claim about the
artifact that only the author can check is not a verified claim.

```bash
python3 docs/papers/gloss/build.py                                        # regenerate the HTML
python3 .claude/skills/paper-gloss/scripts/inject_annotations.py \
        docs/papers/deceptive-grounding-measurable-without-judge-eli5-glossed.html \
        --slug deceptive-grounding-measurable-without-judge                # add the annotation layer
python3 docs/papers/gloss/verify.py                                       # the Phase 3 gate
```

**No dependency outside this repo.** The `paper-gloss` skill these three commands
need is vendored at `.claude/skills/paper-gloss/`, alongside the repo's other
vendored skills and for the reason `CLAUDE.md` gives — so they work in cloud/web
sessions and for collaborators. `verify.py` prefers that in-repo copy and falls
back to a globally-installed skill only if it is missing. Nothing here reads
`$HOME`, adds a package dependency, calls a model, or touches the network.

Deterministic: `build.py` plus the injector reproduce the committed HTML
byte-identically.

| file | role |
|---|---|
| `terms.py` | the 45 approved glossary terms, their match patterns, and the declared `absent`/`from` carve-out |
| `shell.py` | hand-authored CSS + JS (theme tokens, popover, glossary panel, figure lightbox) |
| `build.py` | markdown -> HTML, term-wrapping (longest-match-first), Tier-1 math, base64 figures |
| `verify.py` | the Phase 3 gate; exits non-zero on any failure |
| `check6.py` | per-section `<p>` fidelity vs the markdown's prose blocks |

**Declared carve-outs** (anything not on this list fails the gate):
- `absent` is not wrapped before "from" — `Y's name absent from the answer` is
  ordinary English, not the experimental condition.
- One cross-element bare occurrence: `**80/80 clean** trials` splits the term
  across a `</strong>`. HTML tags cannot overlap, so wrapping it would mean
  moving the source's emphasis, which this rewrite may not do. `verify.py`
  asserts the cross-element hit set equals exactly this list.

This generator is single-use: it assumes one paragraph per non-blank line, no
nested lists, and a `<title>` matching this document's `# ` heading. All three
hold for this source; none is a general markdown contract.
