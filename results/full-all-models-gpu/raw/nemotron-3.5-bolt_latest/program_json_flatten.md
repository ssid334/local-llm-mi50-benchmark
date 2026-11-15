# nemotron-3.5-bolt:latest / program_json_flatten

## Metrics

```json
{
  "wall_s": 5.7382,
  "ttft_s": 1.6943,
  "eval_count": 192,
  "prompt_eval_count": 233,
  "eval_duration_s": 4.0438,
  "prompt_eval_duration_s": 1.4722,
  "load_duration_s": 0.0006,
  "total_duration_s": 5.7377,
  "done_reason": "stop",
  "tokens_per_s": 47.48
}
```

## Response

````text
```python
import json
import sys


def flatten(value, prefix=""):
    if isinstance(value, dict):
        for key in sorted(value):
            yield from flatten(value[key], f"{prefix}.{key}" if prefix else key)
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            yield from flatten(item, f"{prefix}.{idx}" if prefix else str(idx))
    else:
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif value is None:
            rendered = "null"
        elif isinstance(value, (int, float)):
            rendered = json.dumps(value)
        else:
            rendered = value
        yield f"{prefix}={rendered}"


def main():
    data = json.load(sys.stdin)
    for line in sorted(flatten(data)):
        print(line)


if __name__ == "__main__":
    main()
```
````
