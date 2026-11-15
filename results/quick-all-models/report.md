# Local Ollama coding benchmark

- Run: `quick-all-models`
- Started: 2026-11-15T13:31:56.404619+00:00
- Duration: 256.92 s
- Ollama: 0.40.14
- Decoding: temperature=0.0, think=False, num_ctx=8192, seed=42
- Tasks: 8; models: `qwen3.8:latest`, `flint:latest`, `nemotron-3.5-bolt:latest`
- Suite verification: PASS (8 tasks; all references pass, all mutants rejected)

## Leaderboard

| Rank | Model | Overall | Resolved | Coding | SQL/Regex/Tests | Correctness | Edge depth | Median tok/s | Peak VRAM |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `qwen3.8:latest` | 1.000 | 8/8 | 1.000 | 1.000 | 1.000 | 1.000 | 35.70 | 17900 MB |
| 2 | `nemotron-3.5-bolt:latest` | 0.965 | 7/8 | 0.944 | 1.000 | 0.975 | 0.950 | 55.21 | 24965 MB |
| 3 | `flint:latest` | 0.875 | 7/8 | 0.800 | 1.000 | 0.875 | 0.875 | 41.21 | 21555 MB |

## Category scores

| Model | bugfix | codegen | completion | program | refactor | regex | sql | test-generation |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `nemotron-3.5-bolt:latest` | 1.000 | 1.000 | 0.720 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `flint:latest` | 1.000 | 1.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## Per-task results

| Task | Category | Difficulty | `qwen3.8:latest` | `nemotron-3.5-bolt:latest` | `flint:latest` |
|---|---|---|---:|---:|---:|
| codegen_slugify | codegen | easy | 1.00* (11/11) | 1.00* (11/11) | 1.00* (11/11) |
| bugfix_inventory | bugfix | medium | 1.00* (10/10) | 1.00* (10/10) | 1.00* (10/10) |
| completion_parse_duration | completion | medium | 1.00* (10/10) | 0.72 (8/10) | 0.00 (0/10) |
| refactor_summarize | refactor | medium | 1.00* (9/9) | 1.00* (9/9) | 1.00* (9/9) |
| program_word_freq | program | medium | 1.00* (10/10) | 1.00* (10/10) | 1.00* (10/10) |
| sql_top_customers | sql | medium | 1.00* (5/5) | 1.00* (5/5) | 1.00* (5/5) |
| regex_password | regex | medium | 1.00* (14/14) | 1.00* (14/14) | 1.00* (14/14) |
| tests_gen_bank_account | test-generation | hard | 1.00* (kill 100%) | 1.00* (kill 100%) | 1.00* (kill 100%) |

Cells show score plus hidden-check pass count (or mutant kill rate for `test-generation`). `*` means fully resolved.

## Performance on the local GPU

| Model | Load | Median tok/s | Mean TTFT | Eval tokens | Generation wall | Peak VRAM | Mean VRAM delta | Avg GPU use | Max temp | Max power |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 0.00 s | 35.70 | 0.48 s | 1937 | 58.2 s | 17900 MB | 0 MB | 68.5% | 104.0 C | 243.0 W |
| `nemotron-3.5-bolt:latest` | 44.31 s | 55.21 | 1.60 s | 1669 | 42.0 s | 24965 MB | 3 MB | 57.3% | 101.0 C | 241.0 W |
| `flint:latest` | 41.76 s | 41.21 | 0.72 s | 1339 | 38.4 s | 21555 MB | 10 MB | 56.8% | 85.0 C | 149.0 W |

## How validation works

- Every task has hidden basic and edge-case checks. Generated code is executed, not judged by an LLM.
- Score = 0.6 x hidden-check pass rate + 0.4 x edge-case pass rate (plain pass rate when a task has no edge checks). Test-generation uses 0.5 x validity + 0.5 x mutant kill rate, scaled down when fewer than the minimum number of tests are supplied.
- `verify-suite` runs every reference solution (must score 1.0) and every mutant (must score below 1.0). This proves the checks are discriminating.
- Code runs in a bubblewrap sandbox with a read-only root, private /tmp, no network, and CPU/memory/process limits. SQLite queries run read-only.
- Peak VRAM is total device VRAM sampled from rocm-smi and can include other processes on the card. The models are run one at a time; warmup and model load time are excluded from per-task generation metrics.
- Results are a single deterministic-temperature run. GPU kernels can still introduce small numerical differences.
