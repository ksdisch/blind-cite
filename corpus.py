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
N_PAIRS = 80  # M1C power sizing (M1C-BRIEF D2); was 12 at M0, 20 at M1
CORPUS_PATH = Path(__file__).parent / "data" / "corpus.json"
CORPUS_M0_PATH = Path(__file__).parent / "data" / "corpus_m0.json"  # frozen M0 fixture
CORPUS_M1_PATH = Path(__file__).parent / "data" / "corpus_m1.json"  # frozen M1 fixture
N_PAIRS_M0 = 12
N_PAIRS_M1 = 20

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
    # --- M1 extension (p13-p20), APPEND-ONLY (M1-BRIEF D4) ------------------
    # build_corpus indexes THEMES/NAME_PREFIXES by pair position and consumes
    # the RNG strictly in pair order, so appending leaves p01-p12 bit-identical.
    # Inserting, reordering, or editing anything above this line re-rolls M0's
    # frozen corpus; data/corpus_m0.json is the committed guard against that.
    ("streams server-sent events to subscribed clients",
     "a subscriber falls too far behind the event buffer"),
    ("deduplicates records during a bulk ingestion run",
     "a duplicate key survives the merge window"),
    ("throttles outbound webhook deliveries per tenant",
     "a tenant exceeds its delivery quota"),
    ("encrypts field-level data before it is persisted",
     "a data key cannot be unwrapped"),
    ("rebalances shards across a storage cluster",
     "a shard move stalls midway through a transfer"),
    ("renders vector tiles from a geospatial index",
     "a tile request falls outside the indexed extent"),
    ("reconciles inventory counts against an upstream feed",
     "the upstream feed reports a negative count"),
    ("warms a read-through cache ahead of peak traffic",
     "a warm-up pass exceeds its time budget"),
    # --- M1C extension (p21-p80), APPEND-ONLY (M1C-BRIEF D5) ----------------
    # Same mechanics as the M1 append above, one milestone on: 60 new themes
    # and 60 new prefixes, nothing else touched. data/corpus_m1.json is the
    # committed guard for p01-p20 as data/corpus_m0.json is for p01-p12.
    # Authored to avoid version-shaped or identifier-shaped phrasing, so the
    # generator is never nudged into emitting a token the verifier must reject.
    ("batches outbound email into digest deliveries",
     "a digest window closes with no recipients resolved"),
    ("signs outbound requests with a rotating shared secret",
     "a signature timestamp falls outside the accepted skew"),
    ("replays a captured HTTP session against a staging host",
     "a replayed request references an expired session cookie"),
    ("transcodes uploaded audio into a streaming format",
     "an uploaded track carries an unsupported sample rate"),
    ("partitions time-series points into retention buckets",
     "a point arrives older than the oldest retained bucket"),
    ("fans a single publish out to per-subscriber queues",
     "a subscriber queue exceeds its depth limit"),
    ("collapses duplicate alerts into a single incident",
     "an alert arrives after its incident has been resolved"),
    ("snapshots a running container's writable layer",
     "the writable layer changes during the snapshot"),
    ("verifies package signatures before installation",
     "a package signature is made by an untrusted key"),
    ("grants short-lived credentials from a role assumption",
     "a role assumption chain exceeds its maximum depth"),
    ("streams query results without buffering the full set",
     "the client stops reading before the result set ends"),
    ("diffs two configuration trees into an apply plan",
     "a plan would delete a resource marked protected"),
    ("schedules background jobs onto a bounded worker pool",
     "a job outlives the worker pool's shutdown grace period"),
    ("mirrors a remote object store bucket incrementally",
     "a mirrored object changes mid-copy"),
    ("detects clock drift between cluster members",
     "a member's clock drifts beyond the tolerated offset"),
    ("rewrites image URLs to a nearest edge region",
     "no edge region is healthy in the requested continent"),
    ("samples distributed traces at a target rate",
     "a trace is sampled without its parent span"),
    ("expires idle sessions from an in-memory store",
     "an expiry sweep runs while a session is being renewed"),
    ("resolves service endpoints through a discovery registry",
     "the registry returns no healthy endpoint for a service"),
    ("folds streaming aggregates into windowed summaries",
     "an event arrives after its window has been emitted"),
    ("enforces per-key quotas across a request fleet",
     "a key's quota counter cannot be reconciled across nodes"),
    ("renders PDF invoices from a template bundle",
     "a template bundle references a missing font"),
    ("restores a table from an incremental backup chain",
     "a link in the backup chain is missing"),
    ("negotiates a cipher suite during a handshake",
     "the peers share no mutually supported suite"),
    ("pins dependency resolutions into a reproducible lockfile",
     "two dependencies demand mutually exclusive resolutions"),
    ("streams container logs with backpressure",
     "a log consumer falls behind the ring buffer"),
    ("validates uploaded spreadsheets against a column schema",
     "a required column is absent from an upload"),
    ("shards a search index by document locale",
     "a document declares a locale the index does not carry"),
    ("propagates cancellation across nested service calls",
     "a downstream call ignores its cancellation signal"),
    ("rate-limits login attempts per source address",
     "a source address rotates faster than the limiter's window"),
    ("converts geographic coordinates between projections",
     "a coordinate falls outside a projection's valid domain"),
    ("buffers metrics locally during a collector outage",
     "the local buffer fills before the collector returns"),
    ("seals secrets with an envelope encryption key",
     "an envelope key has been revoked"),
    ("orders events by a hybrid logical clock",
     "two events carry identical logical timestamps"),
    ("pre-renders static pages at build time",
     "a page's data source is unavailable at build time"),
    ("auto-scales a worker fleet on queue depth",
     "a scaling action is requested during a cooldown period"),
    ("chunks large uploads into resumable parts",
     "a part's checksum does not match on reassembly"),
    ("masks personal fields in exported datasets",
     "a masking rule matches no column in the export"),
    ("arbitrates leadership among replicas",
     "two replicas claim leadership in the same term"),
    ("prunes unreachable objects from a content store",
     "a prune pass encounters a still-referenced object"),
    ("translates GraphQL selections into database joins",
     "a selection nests deeper than the join budget allows"),
    ("retries idempotent writes after a partition heals",
     "a retried write finds a conflicting revision"),
    ("packs variable-length records into fixed blocks",
     "a record is larger than a single block"),
    ("revalidates cached responses with conditional requests",
     "an origin returns a weak validator where a strong one is required"),
    ("stitches multipart uploads into a single object",
     "a stitch is attempted before every part has landed"),
    ("evaluates feature flags against a user segment",
     "a segment definition references an unknown attribute"),
    ("compresses cold rows into a columnar archive",
     "an archive segment fails its integrity check on read"),
    ("forwards syslog records to a remote collector",
     "a record exceeds the collector's maximum frame size"),
    ("rehydrates an aggregate from its event history",
     "an event in the history fails its schema upgrade"),
    ("balances read traffic across replica lag tiers",
     "every replica exceeds the acceptable lag threshold"),
    ("quarantines files that fail a malware scan",
     "a quarantined file is requested for download"),
    ("assembles a manifest of build artifacts",
     "an artifact is listed twice with differing digests"),
    ("debounces rapid filesystem change notifications",
     "a debounce window closes while a write is still in flight"),
    ("syncs offline edits back to a server copy",
     "two offline edits touch the same field"),
    ("renders a dependency graph into a topological order",
     "the dependency graph contains a cycle"),
    ("issues device certificates during provisioning",
     "a device presents an attestation the issuer cannot verify"),
    ("collects garbage from an interned string table",
     "an interned string is freed while still referenced"),
    ("splits a monolithic export into paged downloads",
     "a page boundary falls inside an indivisible record"),
    ("tags releases from conventional commit messages",
     "a commit message declares an unparseable change type"),
    ("replicates writes to a geographically distant region",
     "a cross-region replication lag budget is exhausted"),
]

NAME_PREFIXES = ["vex", "qua", "zor", "fen", "lum", "dra",
                 "syl", "kro", "bel", "tor", "nim", "pra",
                 # M1 extension (p13-p20), APPEND-ONLY — see the note in THEMES
                 "myr", "sev", "hal", "gri", "vor", "cae", "tyr", "ulm",
                 # M1C extension (p21-p80), APPEND-ONLY — see the note in THEMES
                 "pyr", "sal", "teg", "vun", "wex", "xan", "yol", "zeb",
                 "ard", "bri", "cly", "don", "elu", "fry", "gan", "hes",
                 "ino", "jun", "kel", "lox", "mun", "nex", "oxa", "pel",
                 "quo", "rin", "sto", "tav", "urn", "veg", "wyn", "xer",
                 "yar", "zul", "alk", "bod", "cur", "dex", "esk", "fol",
                 "gum", "hyr", "ilk", "jov", "kir", "lym", "mor", "nyl",
                 "orb", "pum", "riv", "sug", "tul", "uva", "vil", "wor",
                 "xio", "yun", "zim", "gal"]
# FROZEN at M0 (M1-BRIEF D4): NAME_SUFFIXES, VERBS, NOUNS, FLAG_ADJS,
# FLAG_NOUNS and STEM_LETTERS are drawn from by rng.sample/rng.choice, so
# widening ANY of them re-rolls p01-p12 while a generator-vs-itself check would
# still pass. Only THEMES and NAME_PREFIXES may grow, and only by appending.
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


def owner_map(corpus: dict) -> dict[str, dict]:
    """token -> {"name", "pair_id", "role"} for every owned token in the corpus.

    Global ownership, as opposed to the pair-scoped X/Y ownership the M0
    detectors use. Needed only by the M1b detector split, which has to name the
    true owner of a filler token pulled into an answer (M1-BRIEF D2 amended).
    Tokens are globally unique by construction, so this map is well-defined.
    """
    out: dict[str, dict] = {}
    for p in corpus["pairs"]:
        for role in ("x", "y"):
            side = p[role]
            for token in side["tokens"].values():
                out[token] = {"name": side["name"],
                              "pair_id": p["pair_id"], "role": role}
    return out


if __name__ == "__main__":
    corpus = build_corpus()
    CORPUS_PATH.parent.mkdir(exist_ok=True)
    CORPUS_PATH.write_text(json.dumps(corpus, indent=2) + "\n")
    print(f"wrote {CORPUS_PATH} — {corpus['n_pairs']} pairs, "
          f"{len(all_owned_tokens(corpus))} owned tokens, seed {corpus['seed']}")
