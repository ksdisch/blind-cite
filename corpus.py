"""corpus.py — seeded fabricated sibling-library corpus (M0-BRIEF D3).

Each pair is two sibling fabricated libraries (X = queried, Y = alternate) in one
task theme. Each library owns exactly 4 tokens, one per category (method, flag,
error, version). Fabricated names and stems mean zero training-prior
contamination: a token can only enter an answer from a retrieved doc.

Uniqueness invariants (enforced at generation, re-verified in test_corpus.py):
every token globally unique; no token a substring of another; no library name a
substring of another; stems unique per library. Deterministic from SEED — the
committed data/corpus.json is the frozen artifact.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

SEED = 20260715
N_PAIRS = 12
CORPUS_PATH = Path(__file__).parent / "data" / "corpus.json"

# (task — 3rd-person verb phrase completing "which method …",
#  failure — clause completing "raised when …")
THEMES = [
    ("resumes a streaming transfer from a saved checkpoint",
     "a checkpoint fails integrity validation"),
    ("applies exponential backoff to rate-limited API calls",
     "the retry budget is exhausted"),
    ("migrates an embedded database schema in place",
     "a migration step cannot be rolled back"),
    ("caches generated image thumbnails on disk",
     "the cache index becomes corrupted"),
    ("moves undeliverable messages to a dead-letter queue",
     "a message exceeds its redelivery limit"),
    ("rotates TLS certificates without dropping connections",
     "a replacement certificate fails validation"),
    ("hot-reloads configuration without a process restart",
     "a reloaded configuration file fails to parse"),
    ("leases a distributed lock with automatic renewal",
     "a lock lease expires before renewal"),
    ("compacts append-only log segments in the background",
     "a segment checksum mismatch is found during compaction"),
    ("re-establishes dropped websocket connections",
     "the reconnection attempt limit is reached"),
    ("parses cron expressions into scheduled jobs",
     "a cron expression is malformed"),
    ("negotiates payload compression with a remote peer",
     "the peer rejects every offered codec"),
]

NAME_PREFIXES = ["vex", "qua", "zor", "fen", "lum", "dra",
                 "syl", "kro", "bel", "tor", "nim", "pra"]
NAME_SUFFIXES = ["alith", "onor", "effa", "urak", "ilon", "aris",
                 "umet", "enzi", "aroq", "ivex", "olyn", "ettiq",
                 "axen", "obul", "erra", "ustro", "imar", "ovek",
                 "andal", "yric", "ombra", "eshin", "ulfa", "ythar"]

VERBS = ["resume", "restart", "flush", "merge", "split", "drain", "probe",
         "trace", "audit", "prune", "route", "spool", "latch", "weave",
         "chunk", "index", "relay", "scan", "fetch", "purge", "clamp",
         "bloom", "forge", "pivot", "stage", "seal", "batch", "shard",
         "rotate", "lease"]
NOUNS = ["stream", "transfer", "cache", "queue", "ledger", "segment",
         "socket", "payload", "schema", "bundle", "cursor", "buffer",
         "manifest", "snapshot", "channel", "archive", "backlog", "digest",
         "quorum", "replica", "beacon", "tally", "vault", "mesh"]
FLAG_ADJS = ["strict", "eager", "atomic", "durable", "verbose", "adaptive",
             "guarded", "sticky", "rolling", "frozen", "staged", "bounded",
             "chained", "masked", "primed", "salted", "tiered", "woven",
             "zoned", "keyed", "paced", "gated", "pinned", "scoped"]
FLAG_NOUNS = ["mode", "guard", "policy", "window", "budget", "horizon",
              "backoff", "quota", "fence", "margin", "ceiling", "anchor",
              "runway", "cadence", "leash", "collar", "damper", "girdle",
              "tether", "gasket", "keel", "prow", "mast", "hull"]

STEM_LETTERS = "bcdfghjklmnpqrstvwxz"


def _collides(candidate: str, used: set[str]) -> bool:
    return any(candidate in u or u in candidate for u in used)


def _fresh(rng: random.Random, used: set[str], make) -> str:
    for _ in range(10_000):
        candidate = make(rng)
        if not _collides(candidate, used):
            used.add(candidate)
            return candidate
    raise RuntimeError("token space exhausted — widen the pools")


def build_corpus(seed: int = SEED, n_pairs: int = N_PAIRS) -> dict:
    if n_pairs > len(THEMES) or n_pairs > len(NAME_PREFIXES):
        raise ValueError("not enough themes/prefixes for n_pairs")
    rng = random.Random(seed)
    used_tokens: set[str] = set()   # substring-checked pool: all tokens
    used_names: set[str] = set()    # substring-checked pool: library names
    used_stems: set[str] = set()

    def make_stem(r: random.Random) -> str:
        return "".join(r.choice(STEM_LETTERS) for _ in range(3))

    def make_version(r: random.Random) -> str:
        return f"{r.randint(1, 9)}.{r.randint(0, 20)}.{r.randint(0, 20)}"

    pairs = []
    for i in range(n_pairs):
        prefix = NAME_PREFIXES[i]
        suffix_x, suffix_y = rng.sample(NAME_SUFFIXES, 2)
        sides = {}
        for role, suffix in (("x", suffix_x), ("y", suffix_y)):
            name = (prefix + suffix).capitalize()
            if _collides(name, used_names):
                raise RuntimeError(f"name collision: {name}")
            used_names.add(name)
            stem = _fresh(rng, used_stems, make_stem)
            method = _fresh(
                rng, used_tokens,
                lambda r, s=stem: f"{s}_{r.choice(VERBS)}_{r.choice(NOUNS)}")
            flag = _fresh(
                rng, used_tokens,
                lambda r, s=stem: f"{s}.{r.choice(FLAG_ADJS)}_{r.choice(FLAG_NOUNS)}")
            error = _fresh(
                rng, used_tokens,
                lambda r, s=stem: f"{s.upper()}-E{r.randint(100, 999)}")
            version = _fresh(rng, used_tokens, make_version)
            sides[role] = {
                "name": name,
                "stem": stem,
                "tokens": {"method": method, "flag": flag,
                           "error": error, "version": version},
            }
        task, failure = THEMES[i]
        question = (
            f"In the {sides['x']['name']} library, which method {task}, "
            f"which configuration flag must be enabled for it, which error code "
            f"is raised when {failure}, and which version of "
            f"{sides['x']['name']} introduced this feature?"
        )
        pairs.append({
            "pair_id": f"p{i + 1:02d}",
            "theme": {"task": task, "failure": failure},
            "question": question,
            "x": sides["x"],
            "y": sides["y"],
        })
    return {"seed": seed, "n_pairs": n_pairs, "pairs": pairs}


def load_corpus(path: Path = CORPUS_PATH) -> dict:
    return json.loads(path.read_text())


def all_owned_tokens(corpus: dict) -> set[str]:
    return {t for p in corpus["pairs"]
            for side in ("x", "y") for t in p[side]["tokens"].values()}


if __name__ == "__main__":
    corpus = build_corpus()
    CORPUS_PATH.parent.mkdir(exist_ok=True)
    CORPUS_PATH.write_text(json.dumps(corpus, indent=2) + "\n")
    print(f"wrote {CORPUS_PATH} — {corpus['n_pairs']} pairs, "
          f"{len(all_owned_tokens(corpus))} owned tokens, seed {corpus['seed']}")
