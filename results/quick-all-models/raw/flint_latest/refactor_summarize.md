# flint:latest / refactor_summarize

## Metrics

```json
{
  "wall_s": 4.721,
  "ttft_s": 0.8265,
  "eval_count": 160,
  "prompt_eval_count": 298,
  "eval_duration_s": 3.8957,
  "prompt_eval_duration_s": 0.7994,
  "load_duration_s": 0.0006,
  "total_duration_s": 4.7202,
  "done_reason": "stop",
  "tokens_per_s": 41.071
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
