# qwen3.8:latest / sql_top_customers

## Metrics

```json
{
  "wall_s": 4.0881,
  "ttft_s": 0.4695,
  "eval_count": 127,
  "prompt_eval_count": 188,
  "eval_duration_s": 3.6186,
  "prompt_eval_duration_s": 0.2271,
  "load_duration_s": 0.0006,
  "total_duration_s": 4.0876,
  "done_reason": "stop",
  "tokens_per_s": 35.096
}
```

## Response

````text
```sql
WITH customer_totals AS (
    SELECT
        c.name AS customer_name,
        SUM(o.amount) AS total_amount
    FROM customers c
    JOIN orders o ON o.customer_id = c.id
    GROUP BY c.id, c.name
),
ranked AS (
    SELECT
        customer_name,
        total_amount,
        DENSE_RANK() OVER (ORDER BY total_amount DESC) AS dr
    FROM customer_totals
)
SELECT customer_name, total_amount
FROM ranked
WHERE dr <= 2
ORDER BY total_amount DESC, customer_name ASC;
```
````
