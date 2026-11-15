# nemotron-3.5-bolt:latest / sql_top_customers

## Metrics

```json
{
  "wall_s": 3.7761,
  "ttft_s": 1.4944,
  "eval_count": 123,
  "prompt_eval_count": 181,
  "eval_duration_s": 2.2849,
  "prompt_eval_duration_s": 1.2749,
  "load_duration_s": 0.0007,
  "total_duration_s": 3.7755,
  "done_reason": "stop",
  "tokens_per_s": 53.832
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
)
SELECT
    customer_name,
    total_amount
FROM (
    SELECT
        customer_name,
        total_amount,
        DENSE_RANK() OVER (ORDER BY total_amount DESC) AS dr
    FROM customer_totals
)
WHERE dr <= 2
ORDER BY total_amount DESC, customer_name ASC;
```
````
