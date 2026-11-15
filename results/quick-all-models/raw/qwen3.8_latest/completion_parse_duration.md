# qwen3.8:latest / completion_parse_duration

## Metrics

```json
{
  "wall_s": 10.0205,
  "ttft_s": 0.506,
  "eval_count": 351,
  "prompt_eval_count": 214,
  "eval_duration_s": 9.5145,
  "prompt_eval_duration_s": 0.2502,
  "load_duration_s": 0.0006,
  "total_duration_s": 10.0198,
  "done_reason": "stop",
  "tokens_per_s": 36.891
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
        raise ValueError("Input must be a string")
    if not s:
        raise ValueError("Empty string is not a valid duration")
    
    match = _DURATION_RE.match(s)
    if not match:
        raise ValueError(f"Invalid duration: {s!r}")
    
    h_str, m_str, s_str = match.groups()
    
    # At least one unit must be present
    if h_str is None and m_str is None and s_str is None:
        raise ValueError(f"Invalid duration: {s!r}")
    
    h = int(h_str) if h_str is not None else 0
    m = int(m_str) if m_str is not None else 0
    sec = int(s_str) if s_str is not None else 0
    
    return h * 3600 + m * 60 + sec
```
````
