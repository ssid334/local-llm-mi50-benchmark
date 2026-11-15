# qwen3.8:latest / codegen_lru_cache

## Metrics

```json
{
  "wall_s": 11.8516,
  "ttft_s": 1.5174,
  "eval_count": 432,
  "prompt_eval_count": 247,
  "eval_duration_s": 10.3341,
  "prompt_eval_duration_s": 1.3229,
  "load_duration_s": 0.0006,
  "total_duration_s": 11.851,
  "done_reason": "stop",
  "tokens_per_s": 41.803
}
```

## Response

````text
```python
class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.cache = {}
        self.head = None
        self.tail = None

    def _remove_node(self, node):
        prev = node.prev
        next_node = node.next
        if prev:
            prev.next = next_node
        else:
            self.head = next_node
        if next_node:
            next_node.prev = prev
        else:
            self.tail = prev

    def _add_to_head(self, node):
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node
        if not self.tail:
            self.tail = node

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            node = _Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            if len(self.cache) > self.capacity:
                lru = self.tail
                self._remove_node(lru)
                del self.cache[lru.key]


class _Node:
    __slots__ = ('key', 'value', 'prev', 'next')

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
```
````
