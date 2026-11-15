# qwen3.8:latest / codegen_topological_sort

## Metrics

```json
{
  "wall_s": 8.6041,
  "ttft_s": 1.5596,
  "eval_count": 299,
  "prompt_eval_count": 230,
  "eval_duration_s": 7.0444,
  "prompt_eval_duration_s": 1.3596,
  "load_duration_s": 0.0006,
  "total_duration_s": 8.6036,
  "done_reason": "stop",
  "tokens_per_s": 42.445
}
```

## Response

````text
```python
def topo_sort(n, edges):
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Validate node ids
    for u, v in edges:
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(f"Node id out of range: {u} or {v} not in 0..{n-1}")
    
    if n == 0:
        return []
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != n:
        raise ValueError("Graph contains a cycle")
    
    return result
```
````
