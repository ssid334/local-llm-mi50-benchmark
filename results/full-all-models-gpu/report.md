# Local Ollama coding benchmark

- Run: `full-all-models-gpu`
- Started: 2026-11-15T13:55:10.795113+00:00
- Duration: 380.96 s
- Ollama: 0.40.14
- Decoding: temperature=0.0, think=False, num_ctx=8192, seed=42
- Tasks: 15; models: `qwen3.8:latest`, `flint:latest`, `nemotron-3.5-bolt:latest`
- Suite verification: skipped

## Leaderboard

| Rank | Model | Overall | Resolved | Coding | SQL/Regex/Tests | Correctness | Edge depth | Median tok/s | Peak VRAM |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `qwen3.8:latest` | 0.989 | 14/15 | 1.000 | 0.967 | 0.991 | 0.987 | 37.17 | 18188 MB |
| 2 | `nemotron-3.5-bolt:latest` | 0.981 | 14/15 | 0.972 | 1.000 | 0.987 | 0.973 | 57.49 | 25395 MB |
| 3 | `flint:latest` | 0.912 | 12/15 | 0.877 | 0.983 | 0.915 | 0.908 | 29.10 | 17799 MB |

## Category scores

| Model | bugfix | codegen | completion | program | refactor | regex | sql | test-generation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.917 | 1.000 | 1.000 |
| `nemotron-3.5-bolt:latest` | 1.000 | 1.000 | 0.720 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `flint:latest` | 1.000 | 1.000 | 0.000 | 0.883 | 1.000 | 0.959 | 1.000 | 1.000 |

## Per-task results

| Task | Category | Difficulty | `qwen3.8:latest` | `nemotron-3.5-bolt:latest` | `flint:latest` |
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

Cells show score plus hidden-check pass count (or mutant kill rate for `test-generation`). `*` means fully resolved.

## Performance on the local GPU

| Model | Load | Median tok/s | Mean TTFT | Eval tokens | Generation wall | Peak VRAM | Mean VRAM delta | Avg GPU use | Max temp | Max power |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 0.00 s | 37.17 | 1.62 s | 3369 | 117.4 s | 18188 MB | 3 MB | 74.3% | 105.0 C | 258.0 W |
| `nemotron-3.5-bolt:latest` | 18.69 s | 57.49 | 1.66 s | 2635 | 70.7 s | 25395 MB | 2 MB | 64.0% | 104.0 C | 259.0 W |
| `flint:latest` | 38.78 s | 29.10 | 1.55 s | 2252 | 101.8 s | 17799 MB | 5 MB | 53.3% | 75.0 C | 109.0 W |

## How validation works

- Every task has hidden basic and edge-case checks. Generated code is executed, not judged by an LLM.
- Score = 0.6 x hidden-check pass rate + 0.4 x edge-case pass rate (plain pass rate when a task has no edge checks). Test-generation uses 0.5 x validity + 0.5 x mutant kill rate, scaled down when fewer than the minimum number of tests are supplied.
- `verify-suite` runs every reference solution (must score 1.0) and every mutant (must score below 1.0). This proves the checks are discriminating.
- Code runs in a bubblewrap sandbox with a read-only root, private /tmp, no network, and CPU/memory/process limits. SQLite queries run read-only.
- Peak VRAM is total device VRAM sampled from rocm-smi and can include other processes on the card. The models are run one at a time; warmup and model load time are excluded from per-task generation metrics.
- Results are a single deterministic-temperature run. GPU kernels can still introduce small numerical differences.
