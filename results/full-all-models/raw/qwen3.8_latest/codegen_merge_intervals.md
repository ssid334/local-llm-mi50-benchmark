# qwen3.8:latest / codegen_merge_intervals

## Metrics

```json
{
  "wall_s": 30.4085,
  "ttft_s": 6.3447,
  "eval_count": 132,
  "prompt_eval_count": 216,
  "eval_duration_s": 24.0598,
  "prompt_eval_duration_s": 6.158,
  "load_duration_s": 0.0033,
  "total_duration_s": 30.4076,
  "done_reason": "stop",
  "tokens_per_s": 5.486
}
```

## Response

````text
```python
def merge_intervals(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    merged = [list(sorted_intervals[0])]
    
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            # Overlap or touch: merge
            last[1] = max(last[1], current[1])
        else:
            merged.append(list(current))
    
    return merged
```
````
