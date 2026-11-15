# Local Ollama coding benchmark

A self-contained benchmark for local Ollama models, designed for a single AMD
MI50 32 GB (ROCm) card. It focuses on coding tasks and validates the generated
output by **executing it**, not by asking another model to grade it.

The suite has 15 tasks across code generation, bug fixing, completion,
refactoring, standalone programs, SQL, regex, and test generation. Every task
ships with a reference solution and deliberately broken mutants. `verify`
proves that the hidden checks accept the reference and reject every mutant.

## Requirements

- Python 3.11+ (uses only the standard library)
- Ollama running somewhere reachable (default `http://localhost:11434`)
- Bubblewrap (`bwrap`) for strong sandboxing; falls back to plain subprocesses
- `rocm-smi` for GPU VRAM / utilization / temperature / power sampling (optional)
- `prlimit` (util-linux, normally already installed) for memory/CPU/process limits

No Python packages need to be installed.

## Quick start

```bash
# See downloaded models and benchmark tasks
python3 bench.py list

# Prove the task suite is valid. No model calls are made.
python3 bench.py verify

# Fast smoke benchmark: one task per category
python3 bench.py run --quick

# Full 15-task benchmark on the three local models
python3 bench.py run --models qwen3.8:latest,flint:latest,nemotron-3.5-bolt:latest

# Re-render a saved run
python3 bench.py report --input results/<run>/results.json
```

Each run writes `results/<run>/results.json`, `report.md`, and raw model output
under `results/<run>/raw/`.

### Useful options

```bash
--models a,b,c          # comma-separated model names (default: all completion-capable)
--tasks id1,id2         # select specific task ids
--categories codegen,sql
--quick                 # one representative task per category
--think false|true|low|medium|high
--num-ctx 8192          # context window (raise carefully on 32 GB)
--num-predict N         # global cap on generated tokens (never raises a task cap)
--temperature 0 --seed 42
--gpu-device 0          # MI50 is GPU[0] here
--no-gpu                # disable rocm-smi sampling
--sandbox auto|bwrap|subprocess
--keep-loaded           # do not unload between models
--skip-verify           # skip the pre-run reference/mutant verification
--allow-invalid-suite   # run even if suite verification fails
--no-raw                # do not save raw responses
```

## What the tasks validate

| Task | Category | Difficulty | Validation |
|---|---|---|---|
| `codegen_slugify` | codegen | easy | 11 hidden checks incl. unicode, punctuation, empty input |
| `codegen_merge_intervals` | codegen | medium | 10 checks incl. touching intervals, nesting, no mutation |
| `codegen_lru_cache` | codegen | medium | 9 checks incl. recency, capacity 1, invalid capacity |
| `codegen_topological_sort` | codegen | hard | 10 checks incl. cycles, self-loops, duplicate edges |
| `bugfix_binary_search` | bugfix | easy | 11 checks; the buggy mutant infinite-loops and times out |
| `bugfix_inventory` | bugfix | medium | 10 checks incl. insufficient stock and non-positive quantities |
| `completion_parse_duration` | completion | medium | 10 checks incl. unit ordering, duplicates, invalid forms |
| `refactor_summarize` | refactor | medium | 9 checks incl. empty input, floats, one-shot generators |
| `program_json_flatten` | program | medium | 10 stdin/stdout cases incl. empty roots and lexicographic sorting |
| `program_word_freq` | program | medium | 10 cases incl. ties, case folding, ASCII-only words |
| `sql_top_customers` | sql | medium | 5 SQLite result-set cases incl. dense-rank ties |
| `sql_department_above_average` | sql | hard | 5 cases incl. ties, single-employee departments, overall-vs-department average |
| `regex_semver` | regex | medium | 14 match/no-match cases incl. leading zeros and prerelease/build |
| `regex_password` | regex | medium | 14 full-match cases incl. length bounds and forbidden characters |
| `tests_gen_bank_account` | test-generation | hard | generated tests must pass a correct implementation and kill 4 mutants |

Every task also has a reference solution and 3-4 mutants. `verify` executes the
reference (must score 1.0) and each mutant (must score below 1.0). The suite is
not accepted for a run unless all 15 tasks pass this check.

## Scoring

- **Correctness** is the fraction of hidden checks that pass.
- **Edge depth** is the pass rate on checks tagged as edge cases.
- **Score** is `0.6 * correctness + 0.4 * edge_depth` (plain pass rate if a task
  has no edge checks).
- **Test generation** is special: `0.5 * validity + 0.5 * mutant_kill_rate`,
  scaled down if fewer than the requested minimum number of test functions are
  generated.
- A task is **resolved** only when every hidden check passes (and, for test
  generation, all mutants are killed and the minimum test count is met).

The report also shows overall, coding-only, non-coding, correctness, and edge
depth averages, plus per-category and per-task results.

## Execution and isolation

Generated code is executed in a fresh working directory under `/var/tmp` inside
bubblewrap when available:

- read-only host filesystem, with only the task directory writable
- private `/tmp`
- no network namespace
- separate PID/IPC/UTS/cgroup namespaces
- CPU, address-space, process-count, and file-descriptor limits via `prlimit`
- per-test subprocesses with timeouts, so one hanging test does not destroy the
  rest of the result

SQL queries run against an in-memory SQLite database with a read-only authorizer
and a guard that rejects writes, DDL, multiple statements, and non-SELECT/WITH
queries.

## GPU performance metrics

While each request runs, `rocm-smi` is polled for the selected GPU:

- peak total VRAM and VRAM delta from the start of the request
- GPU utilization (max and average)
- max temperature across edge/junction/memory sensors
- max and average socket power
- generation speed (Ollama `eval_count / eval_duration`), time-to-first-token,
  prompt and eval token counts
- model load time from a dedicated warmup request (excluded from task metrics)

`peak_vram_mb` is the **total device** VRAM, so it can include other processes on
the card. Models are run one at a time; the previous model is unloaded before the
next one is warmed up.

## Example results

Full suite (15 tasks), MI50 32 GB, `think=false`, `num_ctx=8192`,
temperature 0, seed 42, single run, 380.96 s total:

| Model | Overall | Resolved | Coding | Median tok/s | Peak VRAM |
|---|---:|---:|---:|---:|---:|
| `qwen3.8:latest` | 0.989 | 14/15 | 1.000 | 37.2 | 17.8 GB |
| `nemotron-3.5-bolt:latest` | 0.981 | 14/15 | 0.972 | 57.5 | 24.8 GB |
| `flint:latest` | 0.912 | 12/15 | 0.877 | 29.1 | 17.4 GB |

Observations from that run:

- All three models fully offloaded their layers to the MI50 during the run:
  qwen 66/66, flint 50/50, nemotron 89/89 plus a 6/6 draft model.
- `qwen3.8` passed every coding category. Its only miss was `regex_semver`:
  the pattern accepted leading-zero versions (`01.2.3`, `1.2.03`), which the
  specification forbids.
- `nemotron-3.5-bolt` was fastest. Its only miss was
  `completion_parse_duration`, where it rejected valid `0s`/`0m` values.
- `flint` missed three tasks: it returned the original TODO scaffold for the
  completion task, scored 8/10 on `program_json_flatten`, and scored 13/14 on
  `regex_semver`.
- A quick suite (8 tasks, one per category) is available with
  `python3 bench.py run --quick`.

These are single-run numbers. For a more robust comparison, run several seeds or
repeat the run and aggregate the JSON results.

## Extending the suite

1. Add a `Task` in `ollama_bench/tasks/` (or a new module).
2. Provide:
   - the prompt,
   - hidden checks,
   - a `reference` output that must score 1.0,
   - at least one `mutants` entry that must score below 1.0.
3. For `kind="tests"`, provide a correct `fixture`, reference tests, and mutant
   implementations.
4. Register the task in `ollama_bench/tasks/__init__.py`.
5. Run `python3 bench.py verify --tasks your_task_id`.

Task kinds:

- `code`: hidden Python test functions run against an extracted `solution.py`
- `program`: complete `main.py`, validated by stdin/stdout cases
- `sql`: extracted query executed against SQLite result-set cases
- `regex`: extracted pattern checked with `re.search`/`re.fullmatch`
- `tests`: generated test file run against a correct fixture and mutants

## Layout

```
bench.py                         CLI
ollama_bench/
  client.py                      Ollama /api/chat streaming + metrics
  extract.py                     code / SQL / regex / test extraction
  metrics.py                     rocm-smi sampler
  sandbox.py                     bubblewrap/prlimit execution
  validators.py                  execution-based validators
  verify.py                      reference/mutant suite verification
  runner.py                      benchmark orchestration
  scoring.py                     model aggregation
  report.py                      Markdown report
  tasks/                         task definitions + references + mutants
results/<run>/                   results.json, report.md, raw/
```

## Caveats

- This is a 15-task coding benchmark, not a general model leaderboard.
- The hidden checks are deliberately strict; a model can be useful and still
  lose points on edge cases.
- GPU results are single-run and temperature-0, but GPU kernels can still be
  numerically nondeterministic.
- `num_ctx` affects KV-cache VRAM. Raising it on 32 GB can cause OOM or eviction.
- Even when every layer is offloaded, Ollama may keep small host-mapped buffers.
  CPU can also spike briefly while the hidden tests execute between generations;
  the GPU is idle during those validation windows.
- Back-to-back model loads can briefly overlap VRAM and make Ollama fall back to
  partial CPU offload. Unload the previous model and let it exit before loading
  the next one; the benchmark does this between models.
- Thinking-level names are model-dependent. `false` and `true` are the safest
  choices; `low`/`medium` may not be accepted by every model.
- `rocm-smi` output formats vary. The sampler parses text output and disables
  itself cleanly if the selected device cannot be read.

## Troubleshooting

- **Cannot reach Ollama**: pass `--host http://host:11434` or set `OLLAMA_HOST`.
- **Sandbox fails**: try `--sandbox subprocess`. This keeps resource limits but
  loses filesystem/network isolation, so only use it for trusted output.
- **OOM / model eviction**: lower `--num-ctx`, unload other GPU processes, or use
  a smaller model.
- **A task times out**: generated code can legitimately hang; the timeout is part
  of the score. Increase `test_timeout` in the task only if the task itself needs
  more time.
- **Suite verification fails**: run `python3 bench.py verify` for per-task
  details. Do not benchmark until references and mutants are behaving correctly.
