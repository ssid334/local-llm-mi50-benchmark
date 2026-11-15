# qwen3.8:latest / sql_top_customers

## Metrics

```json
{
  "wall_s": 5.2718,
  "ttft_s": 1.412,
  "eval_count": 127,
  "prompt_eval_count": 188,
  "eval_duration_s": 3.8597,
  "prompt_eval_duration_s": 1.1706,
  "load_duration_s": 0.0007,
  "total_duration_s": 5.2713,
  "done_reason": "stop",
  "tokens_per_s": 32.904
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
