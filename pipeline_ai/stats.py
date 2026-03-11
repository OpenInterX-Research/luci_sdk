"""Stat helpers for paired developer-study analysis."""

from __future__ import annotations

import math
import random
import statistics
from typing import Iterable


def to_float(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        return float(text)
    except ValueError:
        lowered = text.lower()
        if lowered in {"true", "yes", "y"}:
            return 1.0
        if lowered in {"false", "no", "n"}:
            return 0.0
    return None


def normalize_condition(raw: str) -> str:
    text = (raw or "").strip().lower()
    if "lucia" in text or "with" in text:
        return "lucia"
    if "baseline" in text or "without" in text:
        return "baseline"
    return text


def paired_values(
    rows: list[dict[str, str]],
    metric: str,
    *,
    group_by_task: bool,
) -> list[tuple[float, float]]:
    key_fields = ["participant_id", "task_id"] if group_by_task else ["participant_id"]
    groups: dict[tuple[str, ...], dict[str, float]] = {}
    for row in rows:
        value = to_float(row.get(metric))
        if value is None:
            continue
        cond = normalize_condition(row.get("condition", ""))
        key = tuple((row.get(field) or "").strip() for field in key_fields)
        bucket = groups.setdefault(key, {})
        bucket[cond] = value

    pairs: list[tuple[float, float]] = []
    for group in groups.values():
        if "baseline" in group and "lucia" in group:
            pairs.append((group["baseline"], group["lucia"]))
    return pairs


def _average_ranks(abs_vals: list[float]) -> list[float]:
    indexed = sorted(enumerate(abs_vals), key=lambda item: item[1])
    ranks = [0.0] * len(abs_vals)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[indexed[k][0]] = avg_rank
        i = j
    return ranks


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def wilcoxon_signed_rank(deltas: Iterable[float]) -> dict[str, float]:
    filtered = [float(d) for d in deltas if float(d) != 0.0]
    n = len(filtered)
    if n == 0:
        return {"n": 0.0, "w_pos": 0.0, "w_neg": 0.0, "statistic": 0.0, "z": 0.0, "p_value": 1.0}

    abs_vals = [abs(d) for d in filtered]
    ranks = _average_ranks(abs_vals)
    w_pos = sum(rank for rank, d in zip(ranks, filtered) if d > 0)
    w_neg = sum(rank for rank, d in zip(ranks, filtered) if d < 0)
    statistic = min(w_pos, w_neg)

    mean_w = n * (n + 1) / 4.0
    var_w = n * (n + 1) * (2 * n + 1) / 24.0
    z = 0.0 if var_w <= 0 else (w_pos - mean_w) / math.sqrt(var_w)
    p = max(0.0, min(1.0, 2.0 * (1.0 - _normal_cdf(abs(z)))))
    return {
        "n": float(n),
        "w_pos": float(w_pos),
        "w_neg": float(w_neg),
        "statistic": float(statistic),
        "z": float(z),
        "p_value": float(p),
    }


def rank_biserial(w_pos: float, w_neg: float) -> float:
    denom = w_pos + w_neg
    if denom == 0:
        return 0.0
    return (w_pos - w_neg) / denom


def bootstrap_ci(
    values: list[float],
    *,
    iterations: int = 2000,
    alpha: float = 0.05,
    seed: int = 42,
) -> tuple[float, float]:
    if not values:
        return (0.0, 0.0)
    rng = random.Random(seed)
    samples: list[float] = []
    for _ in range(iterations):
        draw = [values[rng.randrange(len(values))] for _ in range(len(values))]
        samples.append(statistics.median(draw))
    samples.sort()
    low_idx = int((alpha / 2.0) * (len(samples) - 1))
    high_idx = int((1.0 - alpha / 2.0) * (len(samples) - 1))
    return (samples[low_idx], samples[high_idx])


def paired_summary(pairs: list[tuple[float, float]]) -> dict[str, float]:
    if not pairs:
        return {
            "n_pairs": 0.0,
            "median_baseline": 0.0,
            "median_lucia": 0.0,
            "median_delta": 0.0,
            "ci_low": 0.0,
            "ci_high": 0.0,
            "w_stat": 0.0,
            "p_value": 1.0,
            "rank_biserial": 0.0,
        }
    baseline = [p[0] for p in pairs]
    lucia = [p[1] for p in pairs]
    deltas = [l - b for b, l in pairs]
    wil = wilcoxon_signed_rank(deltas)
    ci_low, ci_high = bootstrap_ci(deltas)
    return {
        "n_pairs": float(len(pairs)),
        "median_baseline": float(statistics.median(baseline)),
        "median_lucia": float(statistics.median(lucia)),
        "median_delta": float(statistics.median(deltas)),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "w_stat": float(wil["statistic"]),
        "p_value": float(wil["p_value"]),
        "rank_biserial": float(rank_biserial(wil["w_pos"], wil["w_neg"])),
    }

