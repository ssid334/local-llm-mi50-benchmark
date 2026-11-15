# flint:latest / codegen_slugify

## Metrics

```json
{
  "wall_s": 7.4646,
  "ttft_s": 3.7415,
  "eval_count": 86,
  "prompt_eval_count": 182,
  "eval_duration_s": 3.723,
  "prompt_eval_duration_s": 3.7265,
  "load_duration_s": 0.0027,
  "total_duration_s": 7.463,
  "done_reason": "stop",
  "tokens_per_s": 23.1
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
