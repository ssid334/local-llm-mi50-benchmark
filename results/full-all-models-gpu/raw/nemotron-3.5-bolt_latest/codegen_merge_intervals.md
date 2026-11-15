# nemotron-3.5-bolt:latest / codegen_merge_intervals

## Metrics

```json
{
  "wall_s": 3.6268,
  "ttft_s": 1.5985,
  "eval_count": 112,
  "prompt_eval_count": 218,
  "eval_duration_s": 2.0282,
  "prompt_eval_duration_s": 1.3947,
  "load_duration_s": 0.0017,
  "total_duration_s": 3.6262,
  "done_reason": "stop",
  "tokens_per_s": 55.221
}
```

## Response

````text
```python
def merge_intervals(intervals):
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_intervals[0])]

    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged
```
````
