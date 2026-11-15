# nemotron-3.5-bolt:latest / completion_parse_duration

## Metrics

```json
{
  "wall_s": 6.9696,
  "ttft_s": 1.5768,
  "eval_count": 310,
  "prompt_eval_count": 209,
  "eval_duration_s": 5.3926,
  "prompt_eval_duration_s": 1.3576,
  "load_duration_s": 0.0006,
  "total_duration_s": 6.969,
  "done_reason": "stop",
  "tokens_per_s": 57.486
}
```

## Response

````text
```python
import re

_DURATION_RE = re.compile(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$")


def parse_duration(s: str) -> int:
    """Convert a duration such as '1h30m', '45s', '2m', or '1h' to
    whole seconds.

    Rules:
    - Units are h, m, s and must appear at most once, in that order.
    - At least one unit is required. Units use non-negative integers.
    - No whitespace, signs, decimals, or unknown characters.
    - Raise ValueError for anything invalid.
    """
    if not isinstance(s, str):
        raise ValueError("duration must be a string")

    match = _DURATION_RE.match(s)
    if not match:
        raise ValueError(f"invalid duration: {s!r}")

    hours = int(match.group(1)) if match.group(1) is not None else 0
    minutes = int(match.group(2)) if match.group(2) is not None else 0
    seconds = int(match.group(3)) if match.group(3) is not None else 0

    if hours == 0 and minutes == 0 and seconds == 0:
        raise ValueError(f"invalid duration: {s!r}")

    return hours * 3600 + minutes * 60 + seconds
```
````
