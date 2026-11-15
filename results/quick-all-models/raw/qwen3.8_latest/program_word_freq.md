# qwen3.8:latest / program_word_freq

## Metrics

```json
{
  "wall_s": 5.7296,
  "ttft_s": 0.4955,
  "eval_count": 176,
  "prompt_eval_count": 189,
  "eval_duration_s": 5.234,
  "prompt_eval_duration_s": 0.2436,
  "load_duration_s": 0.0006,
  "total_duration_s": 5.7291,
  "done_reason": "stop",
  "tokens_per_s": 33.626
}
```

## Response

````text
```python
import sys
import re
from collections import Counter

def main():
    data = sys.stdin.read()
    # A word is a maximal run of ASCII letters or digits
    words = re.findall(r'[A-Za-z0-9]+', data)
    if not words:
        return
    # Count in lowercase
    lower_words = [w.lower() for w in words]
    counts = Counter(lower_words)
    # Sort by frequency descending, then lexicographically ascending
    sorted_words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    # Print top 3
    for word, count in sorted_words[:3]:
        print(f"{word} {count}")

if __name__ == "__main__":
    main()
```
````
