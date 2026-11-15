# flint:latest / sql_department_above_average

## Metrics

```json
{
  "wall_s": 3.28,
  "ttft_s": 1.1625,
  "eval_count": 61,
  "prompt_eval_count": 133,
  "eval_duration_s": 2.1174,
  "prompt_eval_duration_s": 1.1405,
  "load_duration_s": 0.0005,
  "total_duration_s": 3.2794,
  "done_reason": "stop",
  "tokens_per_s": 28.809
}
```

## Response

````text
```sql
SELECT e.department, e.name, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary)
    FROM employees e2
    WHERE e2.department = e.department
)
ORDER BY e.department ASC, e.salary DESC, e.name ASC;
```
````
