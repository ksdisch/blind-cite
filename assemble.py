"""assemble.py — controlled-retrieval assembler (M0-BRIEF D4).

The "retrieved doc set" for a trial is deterministically assembled from the
factorial cell — we hand the model exactly the docs the condition specifies.
No vector DB, no embeddings, no learned retriever. Doc order is shuffled by a
pair+cell-seeded RNG (position-confound hygiene) and doc ids are assigned
after the shuffle.
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
