# nemotron-3.5-bolt:latest / sql_department_above_average

## Metrics

```json
{
  "wall_s": 3.0238,
  "ttft_s": 1.4705,
  "eval_count": 94,
  "prompt_eval_count": 148,
  "eval_duration_s": 1.5531,
  "prompt_eval_duration_s": 1.2617,
  "load_duration_s": 0.0007,
  "total_duration_s": 3.0233,
  "done_reason": "stop",
  "tokens_per_s": 60.524
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
