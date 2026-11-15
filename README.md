# Local Ollama coding benchmark – results

## Leaderboard

| Rank | Model | Overall | Resolved | Coding | Non-coding | Correctness | Edge depth | Median tok/s | Peak VRAM |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `qwen3.8:latest` | 0.989 | 14/15 | 1.000 | 0.967 | 0.991 | 0.987 | 37.2 | 18.2 GB |
| 2 | `nemotron-3.5-bolt:latest` | 0.981 | 14/15 | 0.972 | 1.000 | 0.987 | 0.973 | 57.5 | 25.4 GB |
| 3 | `flint:latest` | 0.912 | 12/15 | 0.877 | 0.983 | 0.915 | 0.908 | 29.1 | 17.8 GB |

**Run:** `full-all-models-gpu` · 2026-11-15 · 380.96 s · Ollama 0.40.14 ·
temperature=0, think=false, num_ctx=8192, seed=42 · GPU: AMD MI50 32 GB (ROCm)

## Charts

| Chart | Description |
|---|---|
| [Overall score](results/full-all-models-gpu/chart_overall.png) | Overall benchmark score per model |
| [Category scores](results/full-all-models-gpu/chart_categories.png) | Scores grouped by task category |
| [Performance](results/full-all-models-gpu/chart_performance.png) | Generation speed, TTFT, peak VRAM, max temp |
| [Per-task heatmap](results/full-all-models-gpu/chart_tasks.png) | Score per task per model |

## Category scores

| Model | bugfix | codegen | completion | program | refactor | regex | sql | test-generation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.917 | 1.000 | 1.000 |
| `nemotron-3.5-bolt:latest` | 1.000 | 1.000 | 0.720 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `flint:latest` | 1.000 | 1.000 | 0.000 | 0.883 | 1.000 | 0.959 | 1.000 | 1.000 |

## Per-task results

`*` = fully resolved (all hidden checks passed).

| Task | Category | Difficulty | `qwen3.8` | `nemotron-3.5-bolt` | `flint` |
|---|---|---|---:|---:|---:|
| codegen_slugify | codegen | easy | 1.00* (11/11) | 1.00* (11/11) | 1.00* (11/11) |
| codegen_merge_intervals | codegen | medium | 1.00* (10/10) | 1.00* (10/10) | 1.00* (10/10) |
| codegen_lru_cache | codegen | medium | 1.00* (9/9) | 1.00* (9/9) | 1.00* (9/9) |
| codegen_topological_sort | codegen | hard | 1.00* (10/10) | 1.00* (10/10) | 1.00* (10/10) |
| bugfix_binary_search | bugfix | easy | 1.00* (11/11) | 1.00* (11/11) | 1.00* (11/11) |
| bugfix_inventory | bugfix | medium | 1.00* (10/10) | 1.00* (10/10) | 1.00* (10/10) |
| completion_parse_duration | completion | medium | 1.00* (10/10) | 0.72 (8/10) | 0.00 (0/10) |
| refactor_summarize | refactor | medium | 1.00* (9/9) | 1.00* (9/9) | 1.00* (9/9) |
| program_json_flatten | program | medium | 1.00* (10/10) | 1.00* (10/10) | 0.77 (8/10) |
| program_word_freq | program | medium | 1.00* (10/10) | 1.00* (10/10) | 1.00* (10/10) |
| sql_top_customers | sql | medium | 1.00* (5/5) | 1.00* (5/5) | 1.00* (5/5) |
| sql_department_above_average | sql | hard | 1.00* (5/5) | 1.00* (5/5) | 1.00* (5/5) |
| regex_semver | regex | medium | 0.83 (12/14) | 1.00* (14/14) | 0.92 (13/14) |
| regex_password | regex | medium | 1.00* (14/14) | 1.00* (14/14) | 1.00* (14/14) |
| tests_gen_bank_account | test-generation | hard | 1.00* (kill 100%) | 1.00* (kill 100%) | 1.00* (kill 100%) |

## Performance on the local GPU

| Model | Load (s) | Median tok/s | Mean TTFT (s) | Eval tokens | Gen wall (s) | Peak VRAM | Avg GPU use | Max temp | Max power |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 0.00 | 37.17 | 1.62 | 3369 | 117.4 | 18188 MB | 74.3% | 105.0 C | 258.0 W |
| `nemotron-3.5-bolt:latest` | 18.69 | 57.49 | 1.66 | 2635 | 70.7 | 25395 MB | 64.0% | 104.0 C | 259.0 W |
| `flint:latest` | 38.78 | 29.10 | 1.55 | 2252 | 101.8 | 17799 MB | 53.3% | 75.0 C | 109.0 W |

## Observations

- **qwen3.8:latest** leads overall (0.989). Only miss: `regex_semver` – the pattern
  accepted leading-zero versions (`01.2.3`) which the spec forbids.
- **nemotron-3.5-bolt:latest** is the fastest (57.5 tok/s) with 14/15 resolved.
  Only miss: `completion_parse_duration` – rejected valid `0s`/`0m` values (8/10).
- **flint:latest** missed 3 tasks: `completion_parse_duration` (0/10, returned
  TODO scaffold), `program_json_flatten` (8/10), and `regex_semver` (13/14).

## Regenerating charts

```bash
python3 chart.py results/<run>/results.json
```

Charts are written as PNGs into the same directory as `results.json`.

## Project docs

- [SUITE.md](SUITE.md) – architecture, task suite, scoring, sandbox, and GPU metrics.
- [results/full-all-models-gpu/report.md](results/full-all-models-gpu/report.md) – full per-run report.
