#!/usr/bin/env python3
"""Generate comparison charts from a saved benchmark run.

Reads `results.json` from the run directory and writes PNG charts next to it.
Requires only matplotlib (already a repo dependency via stdlib + matplotlib).
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_results(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def model_names(result: dict) -> list[str]:
    return [m.get("model", "?") for m in result.get("models", [])]


def model_summary(result: dict) -> list[dict]:
    return [m.get("summary", {}) for m in result.get("models", [])]


def _fmt(value, digits=2):
    if value is None:
        return "?"
    return f"{value:.{digits}f}"


def chart_overall(result: dict) -> str:
    models = model_summary(result)
    names = [m["model"] for m in models]
    scores = [m["overall_score"] for m in models]
    resolved = [m["resolved_count"] for m in models]
    total = models[0]["task_count"] if models else 0

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, scores, color=["#4c90d3", "#7a5c95", "#5aa561"], width=0.6)
    for bar, score, resolved_count in zip(bars, scores, resolved):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"{score:.3f}\n({resolved_count}/{total})",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Overall score")
    ax.set_title("Overall benchmark score (higher = better)")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    path = os.path.join(OUT_DIR, "chart_overall.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_categories(result: dict) -> str:
    models = model_summary(result)
    names = [m["model"] for m in models]
    categories = sorted(
        {cat for m in models for cat in m.get("category_scores", {})}
    )
    matrix = np.array(
        [[m.get("category_scores", {}).get(cat, 0.0) for cat in categories]
         for m in models]
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(names))
    width = 0.8 / len(categories)
    for i, cat in enumerate(categories):
        ax.bar(x + (i - len(categories) / 2 + 0.5) * width,
               matrix[:, i], width, label=cat)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Category score")
    ax.set_title("Scores by task category (higher = better)")
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    path = os.path.join(OUT_DIR, "chart_categories.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_performance(result: dict) -> str:
    models = model_summary(result)
    names = [m["model"] for m in models]
    perf = [m.get("performance", {}) for m in models]

    tokens = [p.get("tokens_per_s_median") or 0 for p in perf]
    load = [p.get("load_s") or 0 for p in perf]
    vram = [p.get("peak_vram_mb") or 0 for p in perf]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))

    axes[0].bar(names, tokens, color=["#4c90d3", "#7a5c95", "#5aa561"])
    axes[0].set_title("Median generation speed (tokens/s)")
    axes[0].set_ylabel("tok/s")
    axes[0].grid(axis="y", alpha=0.3)
    axes[0].set_axisbelow(True)
    for i, v in enumerate(tokens):
        axes[0].text(i, v + max(tokens) * 0.02, f"{v:.1f}", ha="center")

    axes[1].bar(names, load, color=["#4c90d3", "#7a5c95", "#5aa561"])
    axes[1].set_title("Model load time (s)")
    axes[1].set_ylabel("s")
    axes[1].grid(axis="y", alpha=0.3)
    axes[1].set_axisbelow(True)
    for i, v in enumerate(load):
        axes[1].text(i, v + max(load) * 0.02 if max(load) else 0.5, f"{v:.1f}", ha="center")

    axes[2].bar(names, vram, color=["#4c90d3", "#7a5c95", "#5aa561"])
    axes[2].set_title("Peak VRAM (MB)")
    axes[2].set_ylabel("MB")
    axes[2].grid(axis="y", alpha=0.3)
    axes[2].set_axisbelow(True)
    for i, v in enumerate(vram):
        axes[2].text(i, v + max(vram) * 0.02 if max(vram) else 50, f"{v:,.0f}", ha="center")

    fig.suptitle("GPU performance comparison (lower load/VRAM = better)", fontsize=12)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    path = os.path.join(OUT_DIR, "chart_performance.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_dashboard(result: dict) -> str:
    models = model_summary(result)
    names = [m["model"] for m in models]
    summaries = [m for m in models]

    fig = plt.figure(figsize=(12, 7))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.35, wspace=0.3)

    ax = fig.add_subplot(gs[0, 0])
    scores = [m["overall_score"] for m in summaries]
    bars = ax.bar(names, scores, color=["#4c90d3", "#7a5c95", "#5aa561"], width=0.6)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Overall score")
    ax.set_title("Overall score")
    for bar, s in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{s:.3f}", ha="center", va="bottom", fontweight="bold")

    ax = fig.add_subplot(gs[0, 1])
    cats = sorted({c for m in summaries for c in m.get("category_scores", {})})
    mat = np.array([[m.get("category_scores", {}).get(c, 0.0) for c in cats] for m in summaries])
    x = np.arange(len(names)); w = 0.8 / len(cats)
    for i, c in enumerate(cats):
        ax.bar(x + (i - len(cats) / 2 + 0.5) * w, mat[:, i], w, label=c)
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=15, ha="right", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Category score")
    ax.set_title("Per-category scores")
    ax.legend(fontsize=7, bbox_to_anchor=(1.0, 1), loc="upper left")
    ax.grid(axis="y", alpha=0.3); ax.set_axisbelow(True)

    ax = fig.add_subplot(gs[1, 0])
    perf = [m.get("performance", {}) for m in summaries]
    toks = [p.get("tokens_per_s_median") or 0 for p in perf]
    ax.bar(names, toks, color=["#4c90d3", "#7a5c95", "#5aa561"])
    ax.set_ylabel("tok/s")
    ax.set_title("Median generation speed")
    for i, v in enumerate(toks):
        ax.text(i, v + max(toks) * 0.02 if max(toks) else 0.5, f"{v:.0f}", ha="center")
    ax.grid(axis="y", alpha=0.3); ax.set_axisbelow(True)

    ax = fig.add_subplot(gs[1, 1])
    vram = [p.get("peak_vram_mb") or 0 for p in perf]
    ax.bar(names, vram, color=["#4c90d3", "#7a5c95", "#5aa561"])
    ax.set_ylabel("MB")
    ax.set_title("Peak VRAM")
    for i, v in enumerate(vram):
        ax.text(i, v + max(vram) * 0.02 if max(vram) else 50, f"{v:,.0f}", rotation=90, ha="center", va="center")
    ax.grid(axis="y", alpha=0.3); ax.set_axisbelow(True)

    fig.suptitle("Model comparison dashboard", fontsize=14, fontweight="bold")
    fig.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.08, hspace=0.35, wspace=0.3)
    path = os.path.join(OUT_DIR, "chart_dashboard.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        candidates = sorted(
            os.path.join(OUT_DIR, d, "results.json")
            for d in os.listdir(OUT_DIR)
            if os.path.isdir(os.path.join(OUT_DIR, d))
            and os.path.exists(os.path.join(OUT_DIR, d, "results.json"))
        )
        input_path = candidates[-1] if candidates else None
    if not input_path or not os.path.exists(input_path):
        print("Usage: chart.py [results.json]", file=sys.stderr)
        print("  (defaults to newest results/*/results.json next to this script)", file=sys.stderr)
        return 2

    result = load_results(input_path)
    paths = [
        chart_overall(result),
        chart_categories(result),
        chart_performance(result),
        chart_dashboard(result),
    ]
    print("Wrote charts to", OUT_DIR)
    for p in paths:
        print("  ", os.path.basename(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
