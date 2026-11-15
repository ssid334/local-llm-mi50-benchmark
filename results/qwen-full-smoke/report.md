# Local Ollama coding benchmark

- Run: `qwen-full-smoke`
- Started: 2026-11-15T13:29:15.721970+00:00
- Duration: 151.61 s
- Ollama: 0.40.14
- Decoding: temperature=0.0, think=False, num_ctx=8192, seed=42
- Tasks: 15; models: `qwen3.8:latest`
- Suite verification: PASS (15 tasks; all references pass, all mutants rejected)

## Leaderboard

| Rank | Model | Overall | Resolved | Coding | SQL/Regex/Tests | Correctness | Edge depth | Median tok/s | Peak VRAM |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `qwen3.8:latest` | 0.989 | 14/15 | 1.000 | 0.967 | 0.991 | 0.987 | 36.55 | 17900 MB |

## Category scores

| Model | bugfix | codegen | completion | program | refactor | regex | sql | test-generation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.917 | 1.000 | 1.000 |

## Per-task results

| Task | Category | Difficulty | `qwen3.8:latest` |
|---|---|---|---:|
| codegen_slugify | codegen | easy | 1.00* (11/11) |
| codegen_merge_intervals | codegen | medium | 1.00* (10/10) |
| codegen_lru_cache | codegen | medium | 1.00* (9/9) |
| codegen_topological_sort | codegen | hard | 1.00* (10/10) |
| bugfix_binary_search | bugfix | easy | 1.00* (11/11) |
| bugfix_inventory | bugfix | medium | 1.00* (10/10) |
| completion_parse_duration | completion | medium | 1.00* (10/10) |
| refactor_summarize | refactor | medium | 1.00* (9/9) |
| program_json_flatten | program | medium | 1.00* (10/10) |
| program_word_freq | program | medium | 1.00* (10/10) |
| sql_top_customers | sql | medium | 1.00* (5/5) |
| sql_department_above_average | sql | hard | 1.00* (5/5) |
| regex_semver | regex | medium | 0.83 (12/14) |
| regex_password | regex | medium | 1.00* (14/14) |
| tests_gen_bank_account | test-generation | hard | 1.00* (kill 100%) |

Cells show score plus hidden-check pass count (or mutant kill rate for `test-generation`). `*` means fully resolved.

## Performance on the local GPU

| Model | Load | Median tok/s | Mean TTFT | Eval tokens | Generation wall | Peak VRAM | Mean VRAM delta | Avg GPU use | Max temp | Max power |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 0.00 s | 36.55 | 1.45 s | 3369 | 115.4 s | 17900 MB | 0 MB | 72.2% | 105.0 C | 248.0 W |

## How validation works

- Every task has hidden basic and edge-case checks. Generated code is executed, not judged by an LLM.
- Score = 0.6 x hidden-check pass rate + 0.4 x edge-case pass rate (plain pass rate when a task has no edge checks). Test-generation uses 0.5 x validity + 0.5 x mutant kill rate, scaled down when fewer than the minimum number of tests are supplied.
- `verify-suite` runs every reference solution (must score 1.0) and every mutant (must score below 1.0). This proves the checks are discriminating.
- Code runs in a bubblewrap sandbox with a read-only root, private /tmp, no network, and CPU/memory/process limits. SQLite queries run read-only.
- Peak VRAM is total device VRAM sampled from rocm-smi and can include other processes on the card. The models are run one at a time; warmup and model load time are excluded from per-task generation metrics.
- Results are a single deterministic-temperature run. GPU kernels can still introduce small numerical differences.
