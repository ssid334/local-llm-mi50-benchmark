# flint:latest / refactor_summarize

## Metrics

```json
{
  "wall_s": 6.9792,
  "ttft_s": 1.5281,
  "eval_count": 160,
  "prompt_eval_count": 298,
  "eval_duration_s": 5.4511,
  "prompt_eval_duration_s": 1.5038,
  "load_duration_s": 0.0007,
  "total_duration_s": 6.9787,
  "done_reason": "stop",
  "tokens_per_s": 29.352
}
```

## Response

````text
```python
def summarize(nums):
    count = 0
    total = 0
    minimum = None
    maximum = None
    for value in nums:
        if count == 0:
            minimum = maximum = value
        else:
            if value < minimum:
                minimum = value
            if value > maximum:
                maximum = value
        count += 1
        total += value
    if count == 0:
        return {"count": 0, "sum": 0, "min": None, "max": None, "mean": None}
    return {
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": total / count,
    }
```
````
