# qwen3.8:latest / bugfix_inventory

## Metrics

```json
{
  "wall_s": 5.3874,
  "ttft_s": 0.4831,
  "eval_count": 195,
  "prompt_eval_count": 249,
  "eval_duration_s": 4.9042,
  "prompt_eval_duration_s": 0.2406,
  "load_duration_s": 0.0006,
  "total_duration_s": 5.3869,
  "done_reason": "stop",
  "tokens_per_s": 39.762
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
            raise ValueError(f"Unknown item: {name}")
        if self.items[name] < qty:
            raise ValueError(f"Not enough stock for item: {name}")
        self.items[name] -= qty

    def count(self, name):
        return self.items.get(name, 0)
```
````
