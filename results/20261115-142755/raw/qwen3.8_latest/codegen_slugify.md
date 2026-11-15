# qwen3.8:latest / codegen_slugify

## Metrics

```json
{
  "wall_s": 38.7227,
  "ttft_s": 34.7924,
  "eval_count": 149,
  "prompt_eval_count": 209,
  "eval_duration_s": 3.9285,
  "prompt_eval_duration_s": 1.5522,
  "load_duration_s": 33.2313,
  "total_duration_s": 38.7222,
  "done_reason": "stop",
  "tokens_per_s": 37.928
}
```

## Response

````text
```python
import re
import unicodedata

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
