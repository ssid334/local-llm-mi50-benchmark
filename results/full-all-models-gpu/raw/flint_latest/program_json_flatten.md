# flint:latest / program_json_flatten

## Metrics

```json
{
  "wall_s": 8.4622,
  "ttft_s": 1.4182,
  "eval_count": 206,
  "prompt_eval_count": 215,
  "eval_duration_s": 7.0438,
  "prompt_eval_duration_s": 1.387,
  "load_duration_s": 0.0005,
  "total_duration_s": 8.4615,
  "done_reason": "stop",
  "tokens_per_s": 29.246
}
```

## Response

````text
```python
import json
import sys


def flatten(value, path=""):
    if isinstance(value, dict):
        if not value:
            return
        for key, val in value.items():
            new_path = f"{path}.{key}" if path else str(key)
            flatten(val, new_path)
    elif isinstance(value, list):
        if not value:
            return
        for i, val in enumerate(value):
            new_path = f"{path}.{i}" if path else str(i)
            flatten(val, new_path)
    else:
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif value is None:
            rendered = "null"
        elif isinstance(value, (int, float)):
            rendered = json.dumps(value)
        else:
            rendered = str(value)
        print(f"{path}={rendered}")


def main():
    data = json.load(sys.stdin)
    flatten(data)


if __name__ == "__main__":
    main()
```
````
