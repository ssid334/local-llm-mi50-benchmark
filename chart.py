#!/usr/bin/env python3
"""Generate comparison charts from a saved benchmark run.

Usage:
    python3 chart.py results/<run>/results.json

Writes PNG charts into the same directory as the input results.json.
Requires matplotlib and numpy (no other third-party dependencies).
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

MODEL_COLORS = ["#4c90d3", "#7a5c95", "#5aa561", "#d37a4c", "#95a55c", "#c95c7a"]


def load_results(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _summaries(result: dict) -> list[dict]:
    return [m.get("summary") or {} for m in result.get("models", [])]


def _colors(n: int) -> list[str]:
    return MODEL_COLORS[:n]


def chart_overall(result: dict, out_dir: str) -> str:
    summaries = _summaries(result)
    names = [s.get("model", "?") for s in summaries]
    scores = [s.get("overall_score", 0.0) or 0.0 for s in summaries]
    resolved = [s.get("resolved_count", 0) or 0 for s in summaries]
    total = summaries[0].get("task_count", 0) if summaries else 0

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, scores, color=_colors(len(names)), width=0.6)
    for bar, score, resolved_count in zip(bars, scores, resolved):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.015,
            f"{score:.3f}\n({resolved_count}/{total} resolved)",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Overall score")
    ax.set_title("Overall benchmark score (higher = better)")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    path = os.path.join(out_dir, "chart_overall.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_categories(result: dict, out_dir: str) -> str:
    summaries = _summaries(result)
    names = [s.get("model", "?") for s in summaries]
    categories = sorted({c for s in summaries for c in s.get("category_scores", {})})
    matrix = np.array(
        [[(s.get("category_scores") or {}).get(c, 0.0) for c in categories]
         for s in summaries],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(names))
    width = 0.8 / len(categories)
    palette = plt.cm.tab10(np.linspace(0, 1, max(len(categories), 2)))
    for i, cat in enumerate(categories):
        ax.bar(
            x + (i - len(categories) / 2 + 0.5) * width,
            matrix[:, i],
            width,
            label=cat,
            color=palette[i],
        )
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15, ha="right")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Category score")
    ax.set_title("Scores by task category (higher = better)")
    ax.legend(title="Category", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    path = os.path.join(out_dir, "chart_categories.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_performance(result: dict, out_dir: str) -> str:
    summaries = _summaries(result)
    names = [s.get("model", "?") for s in summaries]
    perf = [s.get("performance") or {} for s in summaries]

    tokens = [p.get("tokens_per_s_median") or p.get("tokens_per_s_mean") or 0 for p in perf]
    ttft = [p.get("ttft_s_mean") or 0 for p in perf]
    vram = [p.get("peak_vram_mb") or 0 for p in perf]
    temp = [p.get("max_temp_c") or 0 for p in perf]

    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    colors = _colors(len(names))

    def subplot(ax, values, title, ylabel, fmt):
        ax.bar(names, values, color=colors)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.grid(axis="y", alpha=0.3)
        ax.set_axisbelow(True)
        for i, v in enumerate(values):
            ax.text(i, v + max(values) * 0.02 if max(values) else 0.02, fmt.format(v), ha="center")

    subplot(axes[0][0], tokens, "Median generation speed", "tok/s", "{:.1f}")
    subplot(axes[0][1], ttft, "Time to first token", "s", "{:.2f}")
    subplot(axes[1][0], vram, "Peak VRAM", "MB", "{:,.0f}")
    subplot(axes[1][1], temp, "Max GPU temperature", "C", "{:.1f}")

    fig.suptitle("Performance comparison", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0.02, 1, 0.95])
    path = os.path.join(out_dir, "chart_performance.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def chart_tasks(result: dict, out_dir: str) -> str:
    models = result.get("models", [])
    names = [m.get("model", "?") for m in models]
    task_ids = [t.get("task_id", "?") for t in models[0].get("tasks", [])] if models else []
    matrix = np.array(
        [
            [
                (next((t.get("score", 0.0) for t in m.get("tasks", []) if t.get("task_id") == tid), 0.0) or 0.0)
                for tid in task_ids
            ]
            for m in models
        ],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(12, max(4, 0.5 * len(names) + 2)))
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(len(task_ids)))
    ax.set_xticklabels(task_ids, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    for i in range(len(names)):
        for j in range(len(task_ids)):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=7)
    ax.set_title("Per-task scores (1.0 = all checks passed)")
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    fig.tight_layout()
    path = os.path.join(out_dir, "chart_tasks.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 chart.py results/<run>/results.json", file=sys.stderr)
        return 2
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"error: {input_path} not found", file=sys.stderr)
        return 2

    out_dir = os.path.dirname(os.path.abspath(input_path))
    result = load_results(input_path)
    for writer in (chart_overall, chart_categories, chart_performance, chart_tasks):
        path = writer(result, out_dir)
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
