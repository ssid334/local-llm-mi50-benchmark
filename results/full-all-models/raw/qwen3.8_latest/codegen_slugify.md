# qwen3.8:latest / codegen_slugify

## Metrics

```json
{
  "wall_s": 30.0616,
  "ttft_s": 5.3893,
  "eval_count": 149,
  "prompt_eval_count": 209,
  "eval_duration_s": 24.6722,
  "prompt_eval_duration_s": 5.2123,
  "load_duration_s": 0.0068,
  "total_duration_s": 30.0587,
  "done_reason": "stop",
  "tokens_per_s": 6.039
}
```

## Response

````text
```python
import unicodedata
import re

def slugify(text: str) -> str:
    # Normalize unicode to ASCII by removing accents
    normalized = unicodedata.normalize('NFKD', text)
    # Drop remaining non-ASCII characters
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    # Lowercase
    lower = ascii_text.lower()
    # Replace every run of characters that are not ASCII letters or digits with a single hyphen
    slug = re.sub(r'[^a-z0-9]+', '-', lower)
    # Strip leading and trailing hyphens
    slug = slug.strip('-')
    return slug
```
````
