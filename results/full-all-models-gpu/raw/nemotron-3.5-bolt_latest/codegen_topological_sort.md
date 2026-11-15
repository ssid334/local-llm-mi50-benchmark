# nemotron-3.5-bolt:latest / codegen_topological_sort

## Metrics

```json
{
  "wall_s": 5.0436,
  "ttft_s": 1.6189,
  "eval_count": 222,
  "prompt_eval_count": 230,
  "eval_duration_s": 3.4247,
  "prompt_eval_duration_s": 1.4051,
  "load_duration_s": 0.0006,
  "total_duration_s": 5.0432,
  "done_reason": "stop",
  "tokens_per_s": 64.823
}
```

## Response

````text
```python
from collections import deque

def topo_sort(n, edges):
    if n < 0:
        raise ValueError("n must be non-negative")
    
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    
    for u, v in edges:
        if not (0 <= u < n) or not (0 <= v < n):
            raise ValueError("Node id out of range")
        adj[u].append(v)
        indegree[v] += 1
    
    queue = deque([i for i in range(n) if indegree[i] == 0])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != n:
        raise ValueError("Graph contains a cycle")
    
    return order
```
````
