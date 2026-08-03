"""assemble.py — controlled-retrieval assembler (M0-BRIEF D4).

The "retrieved doc set" for a trial is deterministically assembled from the
factorial cell — we hand the model exactly the docs the condition specifies.
No vector DB, no embeddings, no learned retriever. Doc order is shuffled by a
pair+cell-seeded RNG (position-confound hygiene) and doc ids are assigned
after the shuffle.

Two surfaces live here, and M1 measures the difference between them (M1-BRIEF
D3, Option C):

  assemble()             the STARK surface — M0 verbatim, one entity-named
                         title per doc, single Y-doc, prose rendering. M1's
                         arm A (M1a) runs on this, untouched.
  assemble_camouflaged() the CAMOUFLAGE surface (M1b) — one constant title for
                         every doc, k=4 off-theme filler docs, JSON
                         tool-result rendering (the renderer lives in
                         prompts.py). Entity identity appears only inside the
                         content text, per the paper's format.
"""
from __future__ import annotations

import random

from corpus import SEED

CELLS = [
    ("absent", "null_control"),
    ("absent", "completing"),
    ("complete", "null_control"),
    ("complete", "completing"),
]


def cell_id(cx: str, cy: str) -> str:
    return f"{cx}x{cy}"


def assemble(pair: dict, cx: str, cy: str, docs_for_pair: dict) -> list[dict]:
    """(pair, cell) -> ordered retrieved docs [{"doc_id", "title", "text"}].

    `docs_for_pair` is the frozen generated-doc record for this pair_id:
    {"x": text, "y_completing": text, "y_null": text}.
    """
    if (cx, cy) not in CELLS:
        raise ValueError(f"unknown cell: {cx} x {cy}")
    picked: list[tuple[str, str]] = []  # (title, text)
    if cx == "complete":
        picked.append((f"{pair['x']['name']} reference", docs_for_pair["x"]))
    y_key = "y_completing" if cy == "completing" else "y_null"
    y_kind = "reference" if cy == "completing" else "overview"
    picked.append((f"{pair['y']['name']} {y_kind}", docs_for_pair[y_key]))

    rng = random.Random(f"{SEED}:{pair['pair_id']}:{cx}:{cy}")
    rng.shuffle(picked)
    return [
        {"doc_id": f"doc{i + 1}", "title": title, "text": text}
        for i, (title, text) in enumerate(picked)
    ]


# --- M1b camouflage surface (M1-BRIEF D2, as amended) ------------------------

# Title rule, frozen and load-bearing: ONE constant title for every doc. M0's
# titles are entity-name-forward ("<Name> reference"), which would silently
# re-arm the stark surface. No entity names, no theme words, no per-doc
# authoring — nothing to leak and nothing to scan. A stripped *theme-phrase*
# title was considered and rejected: build_corpus interpolates the theme phrase
# verbatim into the question, so an on-theme title would fingerprint the Y-doc
# at both M1 cells in a single title scan and disarm the fillers.
#
# Stated limitation, pre-committed: the constant title is itself a deviation
# from the paper's format (whose `title` exists and is informative, merely not
# entity-labeled), and five byte-identical titles are a synthetic-benchmark tell
# that could REINFORCE the K4 refusal ceiling M1b exists to get past. An M1b
# null cannot be distinguished from M0's on this axis. Documented escalation if
# an M1b null looks title-driven: a small frozen title pool assigned by
# post-shuffle doc POSITION (never by role or theme) — argued at an addendum
# then, never slipped in. The pre-committed default stays constant-title.
CONSTANT_TITLE = "API documentation excerpt"

K_FILLER = 4


def filler_pair_ids(pair_id: str, pair_ids, k: int = K_FILLER) -> list[str]:
    """Which other pairs' X-docs pad this pair's retrieved set.

    Seeded on the PAIR ALONE, deliberately: the filler assignment is then
    identical across the two M1 cells, so the cell contrast stays attributable
    to the Y-doc alone (M1-BRIEF D2 item 2). Every other pair carries a
    different theme by construction (1:1, asserted in test_corpus.py), so every
    filler is off-theme.

    Limitation, stated: off-theme fillers are the only ones the frozen corpus
    can supply without new generation. They buy realistic set length and burial,
    not topical dilution — a model that reads contents can still single out the
    on-theme doc, though with constant titles it must at least read them to do
    so. The next documented camouflage level, if M1b nulls, is same-theme filler
    generation (new docs, new verifier contract) — an addendum, never a slip.
    """
    others = sorted(p for p in pair_ids if p != pair_id)
    if len(others) < k:
        raise ValueError(
            f"need >= {k} other pairs to draw filler from, have {len(others)}")
    return random.Random(f"{SEED}:filler:{pair_id}").sample(others, k)


def assemble_camouflaged(pair: dict, cx: str, cy: str, docs_all: dict,
                         k: int = K_FILLER) -> list[dict]:
    """(pair, cell) -> ordered retrieved docs on the camouflage surface.

    `docs_all` is the whole frozen doc bank keyed by pair_id (not one pair's
    record), because the filler docs are other pairs' X-docs.

    The shuffle is pair-seeded only, so at the two M1 cells — which hold the
    same number of docs and the same fillers — the Y-doc occupies the SAME
    position in both. Position is thus held constant across the contrast rather
    than merely randomized within it.
    """
    if (cx, cy) not in CELLS:
        raise ValueError(f"unknown cell: {cx} x {cy}")
    own = docs_all[pair["pair_id"]]
    texts: list[str] = []
    if cx == "complete":
        texts.append(own["x"])
    texts.append(own["y_completing" if cy == "completing" else "y_null"])
    texts += [docs_all[fid]["x"]
              for fid in filler_pair_ids(pair["pair_id"], docs_all.keys(), k)]

    rng = random.Random(f"{SEED}:m1b:{pair['pair_id']}")
    rng.shuffle(texts)
    return [{"doc_id": f"doc{i + 1}", "title": CONSTANT_TITLE, "text": text}
            for i, text in enumerate(texts)]
