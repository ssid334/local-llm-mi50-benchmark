# qwen3.8:latest / regex_password

## Metrics

```json
{
  "wall_s": 3.4318,
  "ttft_s": 0.4633,
  "eval_count": 89,
  "prompt_eval_count": 159,
  "eval_duration_s": 2.9685,
  "prompt_eval_duration_s": 0.2224,
  "load_duration_s": 0.0006,
  "total_duration_s": 3.4313,
  "done_reason": "stop",
  "tokens_per_s": 29.981
}
```

## Response

````text
```python
r'^(?=[^!@#$%^&*]*[a-z])(?=[^!@#$%^&*]*[A-Z])(?=[^!@#$%^&*]*[0-9])(?=[^!@#$%^&*]*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,32}$'
```
````
