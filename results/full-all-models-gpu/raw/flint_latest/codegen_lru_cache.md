# flint:latest / codegen_lru_cache

## Metrics

```json
{
  "wall_s": 6.4875,
  "ttft_s": 1.4591,
  "eval_count": 143,
  "prompt_eval_count": 220,
  "eval_duration_s": 5.0287,
  "prompt_eval_duration_s": 1.4342,
  "load_duration_s": 0.0006,
  "total_duration_s": 6.487,
  "done_reason": "stop",
  "tokens_per_s": 28.437
}
```

## Response

````text
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```
````
