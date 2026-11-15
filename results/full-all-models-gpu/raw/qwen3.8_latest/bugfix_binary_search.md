# qwen3.8:latest / bugfix_binary_search

## Metrics

```json
{
  "wall_s": 3.6518,
  "ttft_s": 1.5738,
  "eval_count": 94,
  "prompt_eval_count": 254,
  "eval_duration_s": 2.078,
  "prompt_eval_duration_s": 1.3756,
  "load_duration_s": 0.0006,
  "total_duration_s": 3.6514,
  "done_reason": "stop",
  "tokens_per_s": 45.236
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
