"""detectors.py — the four mechanical detectors + outcome taxonomy (M0-BRIEF D6).

Pure regex + set-membership; no model, no network, no LLM judge — the honesty
contract's core clause in code form. Token "shape" is the D3 grammar; ownership
is exact membership in a pair's frozen token map. Doc membership is
extraction-based on both sides (answer tokens and doc tokens run through the
same extractor), so faithfulness/citation/grounding all reduce to set ops.

M1 amendment (M1-BRIEF D2, required not optional): M0's confabulation detector
computed `unowned` pair-scoped — extracted minus X-owned minus Y-owned, with no
intersection against the retrieved set. That was sound only because M0 retrieved
nothing but this pair's own docs, so an unowned token provably could not have
come from a doc. The moment M1b's filler docs enter, every filler token in an
answer would be mislabeled `confabulation` and the soundness argument breaks by
construction. So the set is split, with the scope pinned (T = extracted
token-shaped strings; R = tokens appearing in >=1 retrieved doc; X-owned and
Y-owned stay pair-scoped, exactly as in M0):

    misattributed-other / DG-any  =  (T & R) - X-owned - Y-owned
    confabulation                 =   T - X-owned - Y-owned - R

The two partition M0's `unowned` exactly, so nothing falls through the
precedence table, and under a no-filler design (M0, and M1's stark arm M1a)
`unowned & R` is empty — the narrowed `confabulation` coincides with M0's and
M0's recorded results are untouched. Note the second line's consequence, which
is deliberate: a token globally owned by some *other* pair's library whose doc
was NOT retrieved scores as confabulation, because the model could not have read
it. Ownership does not excuse a token the retrieval never supplied.
"""
from __future__ import annotations

import re

TOKEN_RES = {
    "method": re.compile(r"\b[a-z]{3}_[a-z]{3,10}_[a-z]{3,10}\b(?:\(\))?"),
    "flag": re.compile(r"\b[a-z]{3}\.[a-z]{3,10}_[a-z]{3,10}\b"),
    "error": re.compile(r"\b[A-Z]{3}-E[0-9]{3}\b"),
    "version": re.compile(r"(?<![\d.])\bv?\d+\.\d+\.\d+(?!\.?\d)"),
}

CITATION_RE = re.compile(r"\[(doc\d+)\]", re.IGNORECASE)

REFUSAL_RE = re.compile(
    r"does\s?n[o']t (cover|contain|include|mention|provide|describe)"
    r"|no (information|documentation|mention|details?) (about|on|of|for)"
    r"|not (covered|mentioned|documented|described|provided|available)"
    r"|cannot (find|answer|locate|determine)|can't (find|answer|locate)"
    r"|unable to (find|answer|locate|determine)"
    r"|documentation does not",
    re.IGNORECASE,
)

LABELS = ["DG", "discriminated", "misattributed-other", "confabulation",
          "correct-answer", "correct-refusal", "vague"]


def canonical(category: str, raw: str) -> str:
    if category == "method":
        return raw.removesuffix("()")
    if category == "version":
        return raw.removeprefix("v")
    return raw


def extract_tokens(text: str) -> set[str]:
    """All token-shaped strings in `text`, canonicalized."""
    found = set()
    for category, rx in TOKEN_RES.items():
        for m in rx.findall(text):
            found.add(canonical(category, m))
    return found


def name_present(name: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(name)}\b", text, re.IGNORECASE) is not None


def name_count(name: str, text: str) -> int:
    return len(re.findall(rf"\b{re.escape(name)}\b", text, re.IGNORECASE))


def verify_doc(text: str, doc_type: str, pair: dict) -> list[str]:
    """Mechanical verifier for a generated doc (M0-BRIEF D5). Returns the list
    of contract violations — empty means the doc is accepted. 'No other
    token-shaped strings' is load-bearing: a stray identifier in a doc would
    corrupt both the confabulation detector and the faithfulness proxy."""
    x, y = pair["x"], pair["y"]
    found = extract_tokens(text)
    if doc_type == "x":
        want, subject, forbidden = set(x["tokens"].values()), x, y
    elif doc_type == "y_completing":
        want, subject, forbidden = set(y["tokens"].values()), y, x
    elif doc_type == "y_null":
        want, subject, forbidden = set(), y, x
    else:
        raise ValueError(f"unknown doc_type: {doc_type}")

    violations = []
    if missing := want - found:
        violations.append(f"missing tokens: {sorted(missing)}")
    if extra := found - want:
        violations.append(f"extra token-shaped strings: {sorted(extra)}")
    if name_count(subject["name"], text) < 2:
        violations.append(f"subject name {subject['name']} appears <2x")
    if name_count(forbidden["name"], text) > 0:
        violations.append(f"forbidden name {forbidden['name']} present")
    return violations


def classify(answer: str, pair: dict, docs: list[dict],
             owners: dict | None = None) -> dict:
    """Score one trial answer. `docs` are the retrieved docs the model saw:
    [{"doc_id": "doc1", "text": ...}, ...]. Returns every detector output plus
    the single precedence-assigned label (M0-BRIEF D6, M1-BRIEF D2 amended).

    `owners` is the optional global token -> owner map (corpus.owner_map). It is
    only needed to name the true owner of a misattributed filler token; the
    misattributed/confabulation split itself is pure set algebra and runs either
    way, so M0-era call sites keep working unchanged.
    """
    x_owned = set(pair["x"]["tokens"].values())
    y_owned = set(pair["y"]["tokens"].values())

    tokens = extract_tokens(answer)
    x_tokens = tokens & x_owned
    y_tokens = tokens & y_owned
    unowned = tokens - x_owned - y_owned

    doc_tokens = {d["doc_id"]: extract_tokens(d["text"]) for d in docs}
    retrieved_tokens = set().union(*doc_tokens.values()) if doc_tokens else set()

    # The D2 split: retrieved-but-third-party evidence vs. never-retrieved.
    # These partition `unowned`, so the precedence table stays exhaustive.
    misattributed_other = unowned & retrieved_tokens
    confabulated = unowned - retrieved_tokens

    y_named = name_present(pair["y"]["name"], answer)
    # Owner-name absent/present for the misattributed rung, mirroring the
    # DG/discriminated split. Unknown owners (no map, or a token owned by
    # nobody) cannot be named, so they read as not-named.
    other_owner_names = sorted({
        owners[t]["name"] for t in misattributed_other
        if owners and t in owners})
    other_owner_named = any(name_present(n, answer) for n in other_owner_names)

    # 1. DG detector (DG-Y — the primary, paper-analog measure)
    dg = bool(y_tokens) and not y_named
    # 1b. DG-any (descriptive) — third-party retrieved evidence pulled into the
    # X-answer. Fillers are identical across cells, so this never enters the gate.
    dg_any = bool(misattributed_other)
    # 2. confabulation detector (narrowed: didn't come from the retrieved docs)
    confab = bool(confabulated)
    # 3. faithfulness proxy — every token in the answer appears in SOME retrieved doc
    if tokens:
        faithfulness = "PASS" if tokens <= retrieved_tokens else "FAIL"
    else:
        faithfulness = "NA"
    # 4. citation proxy — cited docs exist and jointly contain every answer token
    cited = [c.lower() for c in CITATION_RE.findall(answer)]
    if tokens:
        cited_tokens = set().union(
            *(doc_tokens[c] for c in cited if c in doc_tokens)) if cited else set()
        citation = ("PASS" if cited and all(c in doc_tokens for c in cited)
                    and tokens <= cited_tokens else "FAIL")
    else:
        citation = "NA"

    grounded = bool(tokens & retrieved_tokens)

    if y_tokens:
        label = "discriminated" if y_named else "DG"
    elif misattributed_other:
        label = "misattributed-other"
    elif confabulated:
        label = "confabulation"
    elif x_tokens:
        label = "correct-answer"
    elif REFUSAL_RE.search(answer):
        label = "correct-refusal"
    else:
        label = "vague"

    return {
        "label": label,
        "dg": dg,
        "dg_any": dg_any,
        "confab": confab,
        "faithfulness": faithfulness,
        "citation": citation,
        "grounded": grounded,
        "y_named": y_named,
        "other_owner_named": other_owner_named,
        "tokens": sorted(tokens),
        "x_tokens": sorted(x_tokens),
        "y_tokens": sorted(y_tokens),
        "unowned_tokens": sorted(unowned),
        "misattributed_other_tokens": sorted(misattributed_other),
        "confabulated_tokens": sorted(confabulated),
        "other_owner_names": other_owner_names,
        "citations": cited,
    }
