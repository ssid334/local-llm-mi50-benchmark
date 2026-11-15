#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import Any

from ollama_bench.client import OllamaClient, OllamaError
from ollama_bench.report import load_result, render_markdown
from ollama_bench.runner import RunConfig, run_benchmark
from ollama_bench.sandbox import Sandbox
from ollama_bench.scoring import summarize_run
from ollama_bench.tasks import ALL_TASKS, CATEGORIES, QUICK_TASK_IDS, TASKS_BY_ID, Task
from ollama_bench.verify import verify_all


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            return cmd_list(args)
        if args.command == "verify":
            return cmd_verify(args)
        if args.command == "run":
            return cmd_run(args)
        if args.command == "report":
            return cmd_report(args)
    except OllamaError as exc:
        print(f"Ollama error: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130
    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Benchmark local Ollama models on validated coding tasks."
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        help="Ollama base URL (default: %(default)s)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List Ollama models and benchmark tasks")
    list_parser.add_argument("--json", action="store_true", help="Emit JSON")

    verify_parser = sub.add_parser(
        "verify", help="Prove the task suite is valid (no model calls)"
    )
    _add_task_selection(verify_parser)
    verify_parser.add_argument(
        "--sandbox",
        choices=["auto", "bwrap", "subprocess"],
        default="auto",
        help="Execution backend (default: %(default)s)",
    )
    verify_parser.add_argument("--json", action="store_true", help="Emit JSON")

    run_parser = sub.add_parser("run", help="Run the benchmark against local models")
    _add_task_selection(run_parser)
    run_parser.add_argument(
        "--models",
        help="Comma-separated model names (default: all completion-capable local models)",
    )
    run_parser.add_argument(
        "--think",
        default="false",
        help="Thinking mode: false, true, low, medium, high (default: false)",
    )
    run_parser.add_argument("--num-ctx", type=int, default=8192)
    run_parser.add_argument(
        "--num-predict",
        type=int,
        default=None,
        help="Global cap on generated tokens (never raises a task's own cap)",
    )
    run_parser.add_argument("--temperature", type=float, default=0.0)
    run_parser.add_argument("--seed", type=int, default=42)
    run_parser.add_argument("--keep-alive", default="45m")
    run_parser.add_argument("--request-timeout", type=float, default=900.0)
    run_parser.add_argument("--gpu-device", type=int, default=0)
    run_parser.add_argument("--no-gpu", action="store_true", help="Disable rocm-smi sampling")
    run_parser.add_argument(
        "--sandbox",
        choices=["auto", "bwrap", "subprocess"],
        default="auto",
        help="Execution backend (default: %(default)s)",
    )
    run_parser.add_argument("--out-dir", default="results")
    run_parser.add_argument("--run-name", default="")
    run_parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip pre-run reference/mutant verification",
    )
    run_parser.add_argument(
        "--allow-invalid-suite",
        action="store_true",
        help="Run even when reference/mutant verification fails",
    )
    run_parser.add_argument(
        "--keep-loaded",
        action="store_true",
        help="Do not unload a model before loading the next one",
    )
    run_parser.add_argument("--no-raw", action="store_true", help="Do not save raw outputs")
    run_parser.add_argument("--quiet", action="store_true")

    report_parser = sub.add_parser("report", help="Render a saved run as Markdown")
    report_parser.add_argument(
        "--input",
        help="Path to results.json (default: newest results/*/results.json)",
    )
    report_parser.add_argument("--out", help="Write Markdown to this path")
    report_parser.add_argument("--json", action="store_true", help="Emit summary JSON")
    return parser


def _add_task_selection(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--tasks",
        help="Comma-separated task ids (see `bench.py list`)",
    )
    parser.add_argument(
        "--categories",
        help=f"Comma-separated categories from: {', '.join(CATEGORIES)}",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run one representative task from each category",
    )


def cmd_list(args: argparse.Namespace) -> int:
    client = OllamaClient(args.host)
    models = client.list_models()
    if args.json:
        print(
            json.dumps(
                {
                    "models": models,
                    "tasks": [
                        {
                            "id": task.id,
                            "title": task.title,
                            "category": task.category,
                            "kind": task.kind,
                            "difficulty": task.difficulty,
                        }
                        for task in ALL_TASKS
                    ],
                },
                indent=2,
            )
        )
        return 0
    print("Ollama models:")
    print(f"  {'NAME':<32} {'SIZE':>8}  {'PARAMS':<10} {'QUANT':<12} MODIFIED")
    for model in models:
        details = model.get("details", {})
        size_gb = model.get("size", 0) / (1024**3)
        print(
            f"  {model.get('name', '?'):<32} {size_gb:>6.1f}GB  "
            f"{details.get('parameter_size', '-'):<10} "
            f"{details.get('quantization_level', '-'):<12} "
            f"{str(model.get('modified_at', ''))[:10]}"
        )
    print("\nBenchmark tasks:")
    print(f"  {'ID':<32} {'CATEGORY':<16} {'KIND':<10} {'DIFF':<8} TITLE")
    for task in ALL_TASKS:
        print(
            f"  {task.id:<32} {task.category:<16} {task.kind:<10} "
            f"{task.difficulty:<8} {task.title}"
        )
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    tasks = _select_tasks(args)
    if not tasks:
        print("No tasks selected.", file=sys.stderr)
        return 2
    sandbox = Sandbox(backend=args.sandbox)
    result = verify_all(tasks, sandbox, verbose=not args.json)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(
            f"\nVerification {'PASSED' if result['ok'] else 'FAILED'}: "
            f"{result['task_count']} tasks, "
            f"{result['surviving_mutants']} surviving mutants, "
            f"{result['duration_s']}s"
        )
    return 0 if result["ok"] else 1


def cmd_run(args: argparse.Namespace) -> int:
    client = OllamaClient(args.host, timeout=args.request_timeout)
    models = _resolve_models(client, args.models)
    if not models:
        print("No completion-capable models found.", file=sys.stderr)
        return 2
    tasks = _select_tasks(args)
    if not tasks:
        print("No tasks selected.", file=sys.stderr)
        return 2
    think = _parse_think(args.think)
    config = RunConfig(
        models=models,
        tasks=tasks,
        think=think,
        num_ctx=args.num_ctx,
        num_predict_cap=args.num_predict,
        temperature=args.temperature,
        seed=args.seed,
        keep_alive=args.keep_alive,
        request_timeout=args.request_timeout,
        gpu_device=args.gpu_device,
        gpu_enabled=not args.no_gpu,
        sandbox_backend=args.sandbox,
        unload_between=not args.keep_loaded,
        skip_verify=args.skip_verify,
        allow_invalid_suite=args.allow_invalid_suite,
        save_raw=not args.no_raw,
        out_dir=args.out_dir,
        run_name=args.run_name,
        quiet=args.quiet,
    )
    result, _run_dir = run_benchmark(client, config)
    if not args.quiet:
        _print_leaderboard(result)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    path = args.input or _latest_result()
    if not path:
        print("No results.json found. Run the benchmark first.", file=sys.stderr)
        return 2
    result = load_result(path)
    if args.json:
        print(
            json.dumps(
                {
                    "meta": result.get("meta", {}),
                    "models": summarize_run(result),
                },
                indent=2,
            )
        )
        return 0
    markdown = render_markdown(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(markdown)
        print(f"Wrote {args.out}")
    else:
        print(markdown)
    return 0


def _select_tasks(args: argparse.Namespace) -> list[Task]:
    ids: list[str]
    if getattr(args, "tasks", None):
        ids = [item.strip() for item in args.tasks.split(",") if item.strip()]
        unknown = [item for item in ids if item not in TASKS_BY_ID]
        if unknown:
            raise RuntimeError(
                f"Unknown task id(s): {', '.join(unknown)}. "
                "Run `python bench.py list` to see available ids."
            )
        tasks = [TASKS_BY_ID[item] for item in ids]
    elif getattr(args, "quick", False):
        tasks = [TASKS_BY_ID[item] for item in QUICK_TASK_IDS]
    else:
        tasks = list(ALL_TASKS)

    categories = getattr(args, "categories", None)
    if categories:
        wanted = {item.strip() for item in categories.split(",") if item.strip()}
        unknown = wanted - set(CATEGORIES)
        if unknown:
            raise RuntimeError(
                f"Unknown categories: {', '.join(sorted(unknown))}. "
                f"Choose from: {', '.join(CATEGORIES)}"
            )
        tasks = [task for task in tasks if task.category in wanted]
    return tasks


def _resolve_models(client: OllamaClient, spec: str | None) -> list[str]:
    if spec:
        return [item.strip() for item in spec.split(",") if item.strip()]
    names: list[str] = []
    for model in client.list_models():
        name = model.get("name")
        if not name:
            continue
        try:
            info = client.show(name)
            capabilities = info.get("capabilities") or []
        except OllamaError:
            capabilities = []
        if not capabilities or "completion" in capabilities:
            names.append(name)
    return names


def _parse_think(value: str) -> bool | str:
    lowered = value.strip().lower()
    if lowered in {"false", "no", "off", "none", "0"}:
        return False
    if lowered in {"true", "yes", "on", "1"}:
        return True
    if lowered in {"low", "medium", "high", "xhigh"}:
        return lowered
    raise RuntimeError(
        "--think must be one of: false, true, low, medium, high, xhigh"
    )


def _latest_result() -> str | None:
    paths = glob.glob(os.path.join("results", "*", "results.json"))
    if not paths:
        return None
    return max(paths, key=os.path.getmtime)


def _print_leaderboard(result: dict[str, Any]) -> None:
    models = summarize_run(result)
    print("\nLeaderboard:")
    print(f"  {'MODEL':<32} {'OVERALL':>8} {'RESOLVED':>10} {'CODING':>8} {'TOK/S':>8}")
    for model in models:
        perf = model.get("performance", {})
        tok_s = perf.get("tokens_per_s_median")
        print(
            f"  {model['model']:<32} {model['overall_score']:>8.3f} "
            f"{model['resolved_count']:>4}/{model['task_count']:<5} "
            f"{model['coding_score']:>8.3f} "
            f"{(f'{tok_s:.2f}' if tok_s is not None else '-'):>8}"
        )


if __name__ == "__main__":
    sys.exit(main())
