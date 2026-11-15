# flint:latest / codegen_topological_sort

## Metrics

```json
{
  "wall_s": 9.0784,
  "ttft_s": 1.4439,
  "eval_count": 221,
  "prompt_eval_count": 209,
  "eval_duration_s": 7.6344,
  "prompt_eval_duration_s": 1.4182,
  "load_duration_s": 0.0006,
  "total_duration_s": 9.0778,
  "done_reason": "stop",
  "tokens_per_s": 28.948
}
```

## Response

````text
```python
from collections import deque, defaultdict

def topo_sort(n, edges):
    if n < 0:
        raise ValueError("n must be non-negative")
    
    for u, v in edges:
        if not (0 <= u < n) or not (0 <= v < n):
            raise ValueError("node id out of range")
    
    adj = defaultdict(set)
    indegree = [0] * n
    
    for u, v in edges:
        if v not in adj[u]:
            adj[u].add(v)
            indegree[v] += 1
    
    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != n:
        raise ValueError("graph contains a cycle")
    
    return result
```
````
