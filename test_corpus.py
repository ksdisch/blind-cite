"""Uniqueness/determinism invariants for the fabricated corpus (M0-BRIEF D3)
plus the M1 (M1-BRIEF D4) and M1C (M1C-BRIEF D5) seed-preservation guards."""
import json

import pytest

from corpus import (CORPUS_M0_PATH, CORPUS_M1_PATH, CORPUS_PATH, N_PAIRS,
                    N_PAIRS_M0, N_PAIRS_M1, all_owned_tokens, build_corpus,
                    owner_map)
from detectors import TOKEN_RES, extract_tokens

DATA = CORPUS_PATH.parent
DOCS_PATH = DATA / "docs.json"
DOCS_M1_PATH = DATA / "docs_m1.json"


@pytest.fixture(scope="module")
def corpus():
    return build_corpus()


def test_deterministic(corpus):
    assert corpus == build_corpus()


def test_frozen_file_matches_generator(corpus):
    frozen = json.loads(CORPUS_PATH.read_text())
    assert frozen == corpus, "data/corpus.json drifted from build_corpus() — regenerate consciously"


def test_tokens_globally_unique_and_substring_free(corpus):
    tokens = sorted(all_owned_tokens(corpus))
    assert len(tokens) == corpus["n_pairs"] * 8
    for i, a in enumerate(tokens):
        for b in tokens[i + 1:]:
            assert a != b
            assert a not in b and b not in a, f"substring collision: {a} / {b}"


def test_names_unique_and_substring_free(corpus):
    names = [p[s]["name"] for p in corpus["pairs"] for s in ("x", "y")]
    assert len(set(names)) == len(names)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            assert a not in b and b not in a


def test_stems_unique(corpus):
    stems = [p[s]["stem"] for p in corpus["pairs"] for s in ("x", "y")]
    assert len(set(stems)) == len(stems)


def test_each_token_matches_exactly_its_category(corpus):
    for p in corpus["pairs"]:
        for side in ("x", "y"):
            for category, token in p[side]["tokens"].items():
                assert extract_tokens(token) == {token}, (category, token)
                for other, rx in TOKEN_RES.items():
                    if other != category:
                        assert not rx.fullmatch(token), (other, token)


def test_question_names_x_only_and_carries_no_tokens(corpus):
    for p in corpus["pairs"]:
        q = p["question"]
        assert p["x"]["name"] in q
        assert p["y"]["name"] not in q
        assert extract_tokens(q) == set(), "question must not leak tokens"


# --- M1 seed preservation (M1-BRIEF D4) -------------------------------------
#
# The extension to 20 pairs is append-only-and-regrow, never a regen. These
# guards have a real referent: data/corpus_m0.json is M0's committed corpus,
# pinned verbatim before the pools grew. If any of them fail, M0's recorded
# evidence (data/pilot.jsonl keys trials by pair_id; its scored.* fields derive
# from doc text) no longer re-verifies from the working tree.

@pytest.fixture(scope="module")
def corpus_m0():
    return json.loads(CORPUS_M0_PATH.read_text())


def test_m0_fixture_is_the_12_pair_corpus(corpus_m0):
    assert corpus_m0["n_pairs"] == N_PAIRS_M0 == 12
    assert len(corpus_m0["pairs"]) == 12


def test_extension_preserves_m0_pairs_verbatim(corpus, corpus_m0):
    """p01-p12 must be byte-identical to the M0 fixture after the pool appends."""
    assert corpus["seed"] == corpus_m0["seed"]
    assert corpus["pairs"][:N_PAIRS_M0] == corpus_m0["pairs"]


def test_extension_preserves_m0_pairs_in_the_frozen_file(corpus_m0):
    frozen = json.loads(CORPUS_PATH.read_text())
    assert frozen["pairs"][:N_PAIRS_M0] == corpus_m0["pairs"]


def test_rebuilding_at_m0_size_reproduces_the_fixture(corpus_m0):
    """The strongest form of the guard: build_corpus(n_pairs=12) at HEAD still
    emits exactly M0's corpus, so nothing below the append point moved."""
    assert build_corpus(n_pairs=N_PAIRS_M0) == corpus_m0


# --- M1C seed preservation (M1C-BRIEF D5) -----------------------------------
#
# The same guard one milestone on. M1C's primary estimand POOLS M1's 20 trials
# per cell with 60 new ones, so it depends on p01-p20 and their doc texts being
# the same artifacts those trials saw — a pool edit anywhere in p13-p20, or a
# gen-docs run that rewrites an existing doc, would silently invalidate the
# pooling. PR #11 review F5 caught the brief claiming this guard already
# existed; data/corpus_m1.json and data/docs_m1.json are it, pinned before the
# pools grew to 80.

@pytest.fixture(scope="module")
def corpus_m1():
    return json.loads(CORPUS_M1_PATH.read_text())


@pytest.fixture(scope="module")
def docs_m1():
    return json.loads(DOCS_M1_PATH.read_text())


def test_m1_fixture_is_the_20_pair_corpus(corpus_m1):
    assert corpus_m1["n_pairs"] == N_PAIRS_M1 == 20
    assert len(corpus_m1["pairs"]) == 20


def test_extension_preserves_m1_pairs_verbatim(corpus, corpus_m1):
    """p01-p20 must be byte-identical to the M1 fixture after the pool appends."""
    assert corpus["seed"] == corpus_m1["seed"]
    assert corpus["pairs"][:N_PAIRS_M1] == corpus_m1["pairs"]


def test_extension_preserves_m1_pairs_in_the_frozen_file(corpus_m1):
    frozen = json.loads(CORPUS_PATH.read_text())
    assert frozen["pairs"][:N_PAIRS_M1] == corpus_m1["pairs"]


def test_rebuilding_at_m1_size_reproduces_the_fixture(corpus_m1):
    assert build_corpus(n_pairs=N_PAIRS_M1) == corpus_m1


def test_m1_doc_texts_are_unchanged(docs_m1):
    """M1's wave rows were scored against these exact strings; gen-docs for
    p21-p80 must not touch them (m1c.py gen-docs asserts the same thing before
    it writes)."""
    live = json.loads(DOCS_PATH.read_text())
    assert len(docs_m1) == N_PAIRS_M1
    for pid, entry in docs_m1.items():
        assert live.get(pid) == entry, pid


def test_extended_to_eighty_pairs(corpus):
    assert corpus["n_pairs"] == N_PAIRS == 80


def test_themes_are_unique_per_pair(corpus):
    """Off-theme filler selection (M1-BRIEF D2 item 2) relies on theme <-> pair
    being 1:1 — any other pair's doc is off-theme by construction."""
    tasks = [p["theme"]["task"] for p in corpus["pairs"]]
    assert len(set(tasks)) == len(tasks)


def test_owner_map_covers_every_token_uniquely(corpus):
    owners = owner_map(corpus)
    assert len(owners) == corpus["n_pairs"] * 8 == len(all_owned_tokens(corpus))
    for p in corpus["pairs"]:
        for role in ("x", "y"):
            for token in p[role]["tokens"].values():
                assert owners[token] == {"name": p[role]["name"],
                                         "pair_id": p["pair_id"], "role": role}
