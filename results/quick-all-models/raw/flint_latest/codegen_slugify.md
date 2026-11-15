# flint:latest / codegen_slugify

## Metrics

```json
{
  "wall_s": 2.7562,
  "ttft_s": 0.7049,
  "eval_count": 86,
  "prompt_eval_count": 182,
  "eval_duration_s": 2.0513,
  "prompt_eval_duration_s": 0.6849,
  "load_duration_s": 0.0051,
  "total_duration_s": 2.753,
  "done_reason": "stop",
  "tokens_per_s": 41.925
}
```

## Response

````text
```python
import re
import unicodedata

def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return slug
```
````
