# Local Ollama coding benchmark

- Run: `vk-full-gpu-test`
- Started: 2026-11-15T13:51:29.139179+00:00
- Duration: 15.45 s
- Ollama: 0.40.14
- Decoding: temperature=0.0, think=False, num_ctx=8192, seed=42
- Tasks: 1; models: `qwen3.8:latest`
- Suite verification: skipped

## Leaderboard

| Rank | Model | Overall | Resolved | Coding | SQL/Regex/Tests | Correctness | Edge depth | Median tok/s | Peak VRAM |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `qwen3.8:latest` | 1.000 | 1/1 | 1.000 | 0.000 | 1.000 | 1.000 | 14.69 | 16393 MB |

## Category scores

| Model | codegen |
|---|---:|
| `qwen3.8:latest` | 1.000 |

## Per-task results

| Task | Category | Difficulty | `qwen3.8:latest` |
|---|---|---|---:|
| codegen_slugify | codegen | easy | 1.00* (11/11) |

Cells show score plus hidden-check pass count (or mutant kill rate for `test-generation`). `*` means fully resolved.

## Performance on the local GPU

| Model | Load | Median tok/s | Mean TTFT | Eval tokens | Generation wall | Peak VRAM | Mean VRAM delta | Avg GPU use | Max temp | Max power |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 0.00 s | 14.69 | 3.07 s | 149 | 13.2 s | 16393 MB | 8 MB | 82.3% | 65.0 C | 164.0 W |

## How validation works

- Every task has hidden basic and edge-case checks. Generated code is executed, not judged by an LLM.
- Score = 0.6 x hidden-check pass rate + 0.4 x edge-case pass rate (plain pass rate when a task has no edge checks). Test-generation uses 0.5 x validity + 0.5 x mutant kill rate, scaled down when fewer than the minimum number of tests are supplied.
- `verify-suite` runs every reference solution (must score 1.0) and every mutant (must score below 1.0). This proves the checks are discriminating.
- Code runs in a bubblewrap sandbox with a read-only root, private /tmp, no network, and CPU/memory/process limits. SQLite queries run read-only.
- Peak VRAM is total device VRAM sampled from rocm-smi and can include other processes on the card. The models are run one at a time; warmup and model load time are excluded from per-task generation metrics.
- Results are a single deterministic-temperature run. GPU kernels can still introduce small numerical differences.
