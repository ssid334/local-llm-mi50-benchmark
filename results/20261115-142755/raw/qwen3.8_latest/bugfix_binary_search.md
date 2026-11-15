# qwen3.8:latest / bugfix_binary_search

## Metrics

```json
{
  "wall_s": 3.6409,
  "ttft_s": 1.5806,
  "eval_count": 94,
  "prompt_eval_count": 254,
  "eval_duration_s": 2.0603,
  "prompt_eval_duration_s": 1.3817,
  "load_duration_s": 0.0048,
  "total_duration_s": 3.6356,
  "done_reason": "stop",
  "tokens_per_s": 45.624
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
