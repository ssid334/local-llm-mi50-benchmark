# qwen3.8:latest / program_json_flatten

## Metrics

```json
{
  "wall_s": 10.7191,
  "ttft_s": 1.6445,
  "eval_count": 294,
  "prompt_eval_count": 239,
  "eval_duration_s": 9.0745,
  "prompt_eval_duration_s": 1.4518,
  "load_duration_s": 0.0006,
  "total_duration_s": 10.7186,
  "done_reason": "stop",
  "tokens_per_s": 32.398
}
```

## Response

````text
```python
import json
import sys


def flatten(value, path):
    leaves = []
    if isinstance(value, dict):
        for k, v in value.items():
            new_path = f"{path}.{k}" if path else k
            leaves.extend(flatten(v, new_path))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            new_path = f"{path}.{i}" if path else str(i)
            leaves.extend(flatten(v, new_path))
    else:
        # Leaf node
        if value is None:
            formatted = "null"
        elif isinstance(value, bool):
            formatted = "true" if value else "false"
        elif isinstance(value, (int, float)):
            # Use JSON number formatting
            formatted = json.dumps(value)
        elif isinstance(value, str):
            formatted = value
        else:
            formatted = json.dumps(value)
        leaves.append((path, formatted))
    return leaves


def main():
    data = sys.stdin.read()
    value = json.loads(data)
    leaves = flatten(value, "")
    leaves.sort(key=lambda x: x[0])
    for path, val in leaves:
        print(f"{path}={val}")


if __name__ == "__main__":
    main()
```
````
