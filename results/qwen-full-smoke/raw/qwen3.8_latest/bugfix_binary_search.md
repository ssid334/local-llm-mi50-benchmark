# qwen3.8:latest / bugfix_binary_search

## Metrics

```json
{
  "wall_s": 2.5738,
  "ttft_s": 0.4723,
  "eval_count": 94,
  "prompt_eval_count": 254,
  "eval_duration_s": 2.1014,
  "prompt_eval_duration_s": 0.2234,
  "load_duration_s": 0.0006,
  "total_duration_s": 2.5734,
  "done_reason": "stop",
  "tokens_per_s": 44.732
}
```

## Response

````text
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```
````
