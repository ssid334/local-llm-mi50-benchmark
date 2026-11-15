# nemotron-3.5-bolt:latest / program_word_freq

## Metrics

```json
{
  "wall_s": 3.554,
  "ttft_s": 1.4597,
  "eval_count": 107,
  "prompt_eval_count": 183,
  "eval_duration_s": 2.0942,
  "prompt_eval_duration_s": 1.258,
  "load_duration_s": 0.0005,
  "total_duration_s": 3.5535,
  "done_reason": "stop",
  "tokens_per_s": 51.093
}
```

## Response

````text
```python
import sys
import re
from collections import Counter

def main() -> None:
    text = sys.stdin.read()
    words = re.findall(r'[A-Za-z0-9]+', text)
    counts = Counter(word.lower() for word in words)

    for word, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:3]:
        print(f"{word} {count}")

if __name__ == "__main__":
    main()
```
````
