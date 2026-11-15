# nemotron-3.5-bolt:latest / bugfix_binary_search

## Metrics

```json
{
  "wall_s": 2.961,
  "ttft_s": 1.6371,
  "eval_count": 82,
  "prompt_eval_count": 241,
  "eval_duration_s": 1.3239,
  "prompt_eval_duration_s": 1.4244,
  "load_duration_s": 0.0007,
  "total_duration_s": 2.9605,
  "done_reason": "stop",
  "tokens_per_s": 61.938
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
