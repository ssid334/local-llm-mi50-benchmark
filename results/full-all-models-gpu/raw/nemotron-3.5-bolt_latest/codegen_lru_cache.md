# nemotron-3.5-bolt:latest / codegen_lru_cache

## Metrics

```json
{
  "wall_s": 3.8873,
  "ttft_s": 1.6371,
  "eval_count": 147,
  "prompt_eval_count": 240,
  "eval_duration_s": 2.25,
  "prompt_eval_duration_s": 1.4296,
  "load_duration_s": 0.0006,
  "total_duration_s": 3.8868,
  "done_reason": "stop",
  "tokens_per_s": 65.333
}
```

## Response

````text
```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
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
