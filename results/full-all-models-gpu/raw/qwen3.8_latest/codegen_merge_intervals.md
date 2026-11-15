# qwen3.8:latest / codegen_merge_intervals

## Metrics

```json
{
  "wall_s": 5.4666,
  "ttft_s": 1.6767,
  "eval_count": 152,
  "prompt_eval_count": 216,
  "eval_duration_s": 3.7899,
  "prompt_eval_duration_s": 1.479,
  "load_duration_s": 0.0008,
  "total_duration_s": 5.4661,
  "done_reason": "stop",
  "tokens_per_s": 40.107
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
    
    for i in range(1, len(sorted_intervals)):
        current_start, current_end = sorted_intervals[i]
        last_start, last_end = merged[-1]
        
        if current_start <= last_end:
            # Overlap or touch: merge
            merged[-1][1] = max(last_end, current_end)
        else:
            merged.append([current_start, current_end])
    
    return merged
```
````
