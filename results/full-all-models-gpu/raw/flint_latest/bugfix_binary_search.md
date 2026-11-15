# flint:latest / bugfix_binary_search

## Metrics

```json
{
  "wall_s": 4.2414,
  "ttft_s": 1.4459,
  "eval_count": 82,
  "prompt_eval_count": 228,
  "eval_duration_s": 2.7954,
  "prompt_eval_duration_s": 1.4175,
  "load_duration_s": 0.0006,
  "total_duration_s": 4.2409,
  "done_reason": "stop",
  "tokens_per_s": 29.334
}
```

## Response

````text
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return -1
```
````
