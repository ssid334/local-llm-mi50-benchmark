# flint:latest / program_word_freq

## Metrics

```json
{
  "wall_s": 5.1573,
  "ttft_s": 1.2822,
  "eval_count": 112,
  "prompt_eval_count": 169,
  "eval_duration_s": 3.8752,
  "prompt_eval_duration_s": 1.2512,
  "load_duration_s": 0.0007,
  "total_duration_s": 5.1567,
  "done_reason": "stop",
  "tokens_per_s": 28.902
}
```

## Response

````text
```python
import sys
import re
from collections import Counter

def main():
    text = sys.stdin.read()
    words = re.findall(r'[A-Za-z0-9]+', text)
    words = [w.lower() for w in words]
    counter = Counter(words)
    top = sorted(counter.items(), key=lambda x: (-x[1], x[0]))[:3]
    for word, count in top:
        print(f"{word} {count}")

if __name__ == "__main__":
    main()
```
````
