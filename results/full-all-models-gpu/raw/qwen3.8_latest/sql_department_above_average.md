# qwen3.8:latest / sql_department_above_average

## Metrics

```json
{
  "wall_s": 3.8008,
  "ttft_s": 1.3352,
  "eval_count": 82,
  "prompt_eval_count": 153,
  "eval_duration_s": 2.4655,
  "prompt_eval_duration_s": 1.1398,
  "load_duration_s": 0.004,
  "total_duration_s": 3.8002,
  "done_reason": "stop",
  "tokens_per_s": 33.259
}
```

## Response

````text
```sql
WITH dept_avg AS (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
)
SELECT e.department, e.name, e.salary
FROM employees e
JOIN dept_avg d ON e.department = d.department
WHERE e.salary > d.avg_salary
ORDER BY e.department ASC, e.salary DESC, e.name ASC;
```
````
