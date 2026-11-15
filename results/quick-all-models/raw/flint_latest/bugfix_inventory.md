# flint:latest / bugfix_inventory

## Metrics

```json
{
  "wall_s": 4.926,
  "ttft_s": 0.7483,
  "eval_count": 174,
  "prompt_eval_count": 225,
  "eval_duration_s": 4.1776,
  "prompt_eval_duration_s": 0.726,
  "load_duration_s": 0.0006,
  "total_duration_s": 4.9255,
  "done_reason": "stop",
  "tokens_per_s": 41.651
}
```

## Response

````text
```python
class Inventory:
    def __init__(self):
        self.items = {}

    def add(self, name, qty):
        if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
            raise ValueError("Quantity must be a positive integer")
        self.items[name] = self.items.get(name, 0) + qty

    def remove(self, name, qty):
        if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
            raise ValueError("Quantity must be a positive integer")
        if name not in self.items or self.items[name] < qty:
            raise ValueError("Insufficient stock or unknown item")
        self.items[name] -= qty

    def count(self, name):
        return self.items.get(name, 0)
```
````
