# flint:latest / codegen_merge_intervals

## Metrics

```json
{
  "wall_s": 5.4922,
  "ttft_s": 1.4553,
  "eval_count": 102,
  "prompt_eval_count": 194,
  "eval_duration_s": 4.0368,
  "prompt_eval_duration_s": 1.4335,
  "load_duration_s": 0.0005,
  "total_duration_s": 5.4916,
  "done_reason": "stop",
  "tokens_per_s": 25.268
}
```

## Response

````text
```python
def merge_intervals(intervals):
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for start, end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = [last_start, max(last_end, end)]
        else:
            merged.append([start, end])

    return merged
```
````
