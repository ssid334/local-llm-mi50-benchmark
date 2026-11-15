# qwen3.8:latest / regex_password

## Metrics

```json
{
  "wall_s": 4.538,
  "ttft_s": 1.3653,
  "eval_count": 89,
  "prompt_eval_count": 159,
  "eval_duration_s": 3.1725,
  "prompt_eval_duration_s": 1.1614,
  "load_duration_s": 0.0006,
  "total_duration_s": 4.5375,
  "done_reason": "stop",
  "tokens_per_s": 28.054
}
```

## Response

````text
```python
r'^(?=[^!@#$%^&*]*[a-z])(?=[^!@#$%^&*]*[A-Z])(?=[^!@#$%^&*]*[0-9])(?=[^!@#$%^&*]*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,32}$'
```
````
