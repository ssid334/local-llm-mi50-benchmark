# flint:latest / program_word_freq

## Metrics

```json
{
  "wall_s": 3.3969,
  "ttft_s": 0.6886,
  "eval_count": 112,
  "prompt_eval_count": 169,
  "eval_duration_s": 2.7084,
  "prompt_eval_duration_s": 0.6567,
  "load_duration_s": 0.0007,
  "total_duration_s": 3.3964,
  "done_reason": "stop",
  "tokens_per_s": 41.353
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
