# qwen3.8:latest / regex_password

## Metrics

```json
{
  "wall_s": 4.5038,
  "ttft_s": 1.3205,
  "eval_count": 89,
  "prompt_eval_count": 159,
  "eval_duration_s": 3.1833,
  "prompt_eval_duration_s": 1.1367,
  "load_duration_s": 0.0006,
  "total_duration_s": 4.5032,
  "done_reason": "stop",
  "tokens_per_s": 27.958
}
```

## Response

````text
```python
r'^(?=[^!@#$%^&*]*[a-z])(?=[^!@#$%^&*]*[A-Z])(?=[^!@#$%^&*]*[0-9])(?=[^!@#$%^&*]*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,32}$'
```
````
