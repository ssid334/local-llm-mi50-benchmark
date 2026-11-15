# nemotron-3.5-bolt:latest / bugfix_inventory

## Metrics

```json
{
  "wall_s": 4.4929,
  "ttft_s": 1.6563,
  "eval_count": 176,
  "prompt_eval_count": 237,
  "eval_duration_s": 2.8365,
  "prompt_eval_duration_s": 1.4495,
  "load_duration_s": 0.0007,
  "total_duration_s": 4.4924,
  "done_reason": "stop",
  "tokens_per_s": 62.048
}
```

## Response

````text
```python
class Inventory:
    def __init__(self):
        self.items = {}

    def _validate_qty(self, qty):
        if not isinstance(qty, int) or isinstance(qty, bool) or qty <= 0:
            raise ValueError("qty must be a positive integer")

    def add(self, name, qty):
        self._validate_qty(qty)
        self.items[name] = self.items.get(name, 0) + qty

    def remove(self, name, qty):
        self._validate_qty(qty)
        if name not in self.items:
            raise ValueError("unknown item")
        if self.items[name] < qty:
            raise ValueError("not enough stock")
        self.items[name] -= qty

    def count(self, name):
        return self.items.get(name, 0)
```
````
