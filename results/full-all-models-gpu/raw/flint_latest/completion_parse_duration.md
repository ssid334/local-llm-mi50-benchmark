# flint:latest / completion_parse_duration

## Metrics

```json
{
  "wall_s": 5.9216,
  "ttft_s": 1.4154,
  "eval_count": 133,
  "prompt_eval_count": 192,
  "eval_duration_s": 4.5061,
  "prompt_eval_duration_s": 1.388,
  "load_duration_s": 0.0006,
  "total_duration_s": 5.9211,
  "done_reason": "stop",
  "tokens_per_s": 29.516
}
```

## Response

````text
```python
import re

_DURATION_RE = re.compile(r"TODO")


def parse_duration(s: str) -> int:
    """Convert a duration such as '1h30m', '45s', '2m', or '1h' to
    whole seconds.

    Rules:
    - Units are h, m, s and must appear at most once, in that order.
    - At least one unit is required. Units use non-negative integers.
    - No whitespace, signs, decimals, or unknown characters.
    - Raise ValueError for anything invalid.
    """
    # TODO: implement
    raise NotImplementedError
```
````
