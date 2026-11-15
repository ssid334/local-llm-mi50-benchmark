# flint:latest / tests_gen_bank_account

## Metrics

```json
{
  "wall_s": 13.5075,
  "ttft_s": 0.7873,
  "eval_count": 518,
  "prompt_eval_count": 272,
  "eval_duration_s": 12.7202,
  "prompt_eval_duration_s": 0.7664,
  "load_duration_s": 0.0007,
  "total_duration_s": 13.507,
  "done_reason": "stop",
  "tokens_per_s": 40.723
}
```

## Response

````text
```python
from solution import BankAccount


def test_initial_balance_is_zero_by_default():
    account = BankAccount()
    assert account.get_balance() == 0


def test_initial_balance_can_be_set_to_non_negative_integer():
    account = BankAccount(100)
    assert account.get_balance() == 100


def test_negative_initial_balance_raises_value_error():
    try:
        BankAccount(-1)
        assert False, "Expected ValueError for negative initial balance"
    except ValueError:
        pass


def test_deposit_increases_balance():
    account = BankAccount(50)
    account.deposit(25)
    assert account.get_balance() == 75


def test_deposit_with_invalid_amount_raises_value_error_and_keeps_balance():
    account = BankAccount(30)
    try:
        account.deposit(0)
        assert False, "Expected ValueError for zero deposit"
    except ValueError:
        pass
    assert account.get_balance() == 30

    try:
        account.deposit(-5)
        assert False, "Expected ValueError for negative deposit"
    except ValueError:
        pass
    assert account.get_balance() == 30

    try:
        account.deposit(2.5)
        assert False, "Expected ValueError for non-integer deposit"
    except ValueError:
        pass
    assert account.get_balance() == 30


def test_withdraw_decreases_balance():
    account = BankAccount(80)
    account.withdraw(30)
    assert account.get_balance() == 50


def test_withdraw_more_than_balance_raises_value_error_and_keeps_balance():
    account = BankAccount(20)
    try:
        account.withdraw(50)
        assert False, "Expected ValueError for overdraw"
    except ValueError:
        pass
    assert account.get_balance() == 20


def test_withdraw_with_invalid_amount_raises_value_error_and_keeps_balance():
    account = BankAccount(40)
    try:
        account.withdraw(0)
        assert False, "Expected ValueError for zero withdraw"
    except ValueError:
        pass
    assert account.get_balance() == 40

    try:
        account.withdraw(-10)
        assert False, "Expected ValueError for negative withdraw"
    except ValueError:
        pass
    assert account.get_balance() == 40

    try:
        account.withdraw(3.5)
        assert False, "Expected ValueError for non-integer withdraw"
    except ValueError:
        pass
    assert account.get_balance() == 40
```
````
