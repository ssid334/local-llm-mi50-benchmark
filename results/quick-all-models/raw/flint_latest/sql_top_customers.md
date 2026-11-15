# flint:latest / sql_top_customers

## Metrics

```json
{
  "wall_s": 3.4102,
  "ttft_s": 0.6716,
  "eval_count": 112,
  "prompt_eval_count": 166,
  "eval_duration_s": 2.7384,
  "prompt_eval_duration_s": 0.6494,
  "load_duration_s": 0.0006,
  "total_duration_s": 3.4096,
  "done_reason": "stop",
  "tokens_per_s": 40.9
}
```

## Response

````text
```sql
WITH customer_totals AS (
    SELECT c.name AS customer_name, SUM(o.amount) AS total_amount
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name
),
ranked AS (
    SELECT customer_name, total_amount,
           DENSE_RANK() OVER (ORDER BY total_amount DESC) AS dr
    FROM customer_totals
)
SELECT customer_name, total_amount
FROM ranked
WHERE dr <= 2
ORDER BY total_amount DESC, customer_name ASC;
```
````
