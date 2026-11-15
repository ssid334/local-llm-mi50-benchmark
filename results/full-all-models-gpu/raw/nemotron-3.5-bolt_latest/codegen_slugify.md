# nemotron-3.5-bolt:latest / codegen_slugify

## Metrics

```json
{
  "wall_s": 3.7371,
  "ttft_s": 1.5865,
  "eval_count": 96,
  "prompt_eval_count": 203,
  "eval_duration_s": 2.1506,
  "prompt_eval_duration_s": 1.3867,
  "load_duration_s": 0.0008,
  "total_duration_s": 3.7367,
  "done_reason": "stop",
  "tokens_per_s": 44.639
}
```

## Response

````text
```python
import unicodedata
import re

def slugify(text: str) -> str:
    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = ''.join(ch for ch in normalized if ord(ch) < 128)
    lowered = ascii_text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', lowered).strip('-')
    return slug
```
````
