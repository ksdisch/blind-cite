"""client.py — thin OpenRouter wrapper with a hard-capped cost meter.

Lineage pattern (decay-pin → lossy-wall → ghost-patch), rewritten for this
repo: loud missing-key error, bounded retries, model slug required per call,
measured cost per call. Prices are per-M-token rates pulled live 2026-07-15
(docs/M0-BRIEF.md D2); `m0.py ping` re-verifies slugs + prices before any wave
spends. The meter enforces the D8 wave caps — it checks BEFORE each call and
halts the wave when the cap is reached.
"""
from __future__ import annotations

import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

ROSTER = [  # D2, pre-committed 2026-07-15
    "qwen/qwen-2.5-7b-instruct",
    "meta-llama/llama-3.1-8b-instruct",
    "google/gemma-3-12b-it",
]
BENCH = [  # promotion order (D7 roster floor)
    "openai/gpt-oss-20b",
    "qwen/qwen3-14b",
]
GENERATOR = "openai/gpt-4o-mini"  # fixed, non-roster, never graded

PRICES = {  # $ per 1M tokens (input, output) — openrouter.ai/api/v1/models
    # Re-pinned 2026-08-03 at `m1.py ping` before M1 spent anything. Two slugs
    # had drifted since the M0 pin; the roster itself is unchanged (every D2
    # slug still exists), so this is meter accuracy, not a design change. M0's
    # recorded per-call costs in data/pilot.jsonl were measured under the old
    # rates and stay as the historical fact they are.
    "qwen/qwen-2.5-7b-instruct": (0.10, 0.20),   # drift: was (0.04, 0.10)
    "meta-llama/llama-3.1-8b-instruct": (0.05, 0.08),
    "google/gemma-3-12b-it": (0.05, 0.15),
    "openai/gpt-oss-20b": (0.03, 0.13),
    "qwen/qwen3-14b": (0.2275, 0.91),            # drift: was (0.10, 0.24)
    "openai/gpt-4o-mini": (0.15, 0.60),
}

SUBJECT_MAX_TOKENS = 400
SUBJECT_TEMPERATURE = 0.0  # D2: deterministic-as-available subjects
GENERATOR_TEMPERATURE = 0.8  # doc variety; docs are verified + frozen anyway


class BudgetExceeded(RuntimeError):
    pass


class CostMeter:
    def __init__(self, cap_usd: float):
        self.cap = cap_usd
        self.total = 0.0
        self.calls = 0

    def check(self):
        if self.total >= self.cap:
            raise BudgetExceeded(
                f"cost meter at ${self.total:.4f} >= cap ${self.cap:.2f}")

    def add(self, cost: float):
        self.total += cost
        self.calls += 1


def _client() -> OpenAI:
    load_dotenv()
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("OPENROUTER_API_KEY missing — put it in .env (never commit it)")
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key, timeout=120)


_OAI: OpenAI | None = None


def chat(
    model: str,
    prompt: str,
    *,
    max_tokens: int = SUBJECT_MAX_TOKENS,
    temperature: float = SUBJECT_TEMPERATURE,
    meter: CostMeter | None = None,
    retries: int = 3,
) -> dict:
    """One user-turn completion. Returns text + usage + measured cost.

    Retries transient failures with backoff (incl. OpenRouter's occasional
    malformed-body JSONDecodeError, observed in the ghost-patch waves)."""
    global _OAI
    if _OAI is None:
        _OAI = _client()
    if meter:
        meter.check()
    t0 = time.monotonic()
    for attempt in range(retries):
        try:
            resp = _OAI.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            break
        except (RateLimitError, APITimeoutError, APIError, json.JSONDecodeError):
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    u = resp.usage
    pin, pout = PRICES[model]
    cost = (u.prompt_tokens * pin + u.completion_tokens * pout) / 1e6
    if meter:
        meter.add(cost)
    return {
        "model": model,
        "text": resp.choices[0].message.content or "",
        "prompt_tokens": u.prompt_tokens,
        "completion_tokens": u.completion_tokens,
        "cost": cost,
        "seconds": round(time.monotonic() - t0, 2),
        "finish_reason": resp.choices[0].finish_reason,
    }


def ping_models() -> list[str]:
    """Verify every roster/bench/generator slug still exists on OpenRouter and
    the pinned prices still match. Returns a list of drift messages (empty =
    clean). Any drift must be resolved consciously before a wave spends."""
    import urllib.request

    with urllib.request.urlopen("https://openrouter.ai/api/v1/models") as r:
        live = {m["id"]: m.get("pricing", {}) for m in json.load(r)["data"]}
    problems = []
    for slug, (pin, pout) in PRICES.items():
        if slug not in live:
            problems.append(f"MISSING slug: {slug}")
            continue
        lp = (round(float(live[slug].get("prompt", 0)) * 1e6, 4),
              round(float(live[slug].get("completion", 0)) * 1e6, 4))
        if lp != (pin, pout):
            problems.append(f"PRICE DRIFT {slug}: pinned {(pin, pout)} live {lp}")
    return problems
