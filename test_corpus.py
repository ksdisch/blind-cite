"""Uniqueness/determinism invariants for the fabricated corpus (M0-BRIEF D3)."""
import json

import pytest

from corpus import CORPUS_PATH, all_owned_tokens, build_corpus
from detectors import TOKEN_RES, extract_tokens


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
