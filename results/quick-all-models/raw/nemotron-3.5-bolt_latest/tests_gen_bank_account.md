# nemotron-3.5-bolt:latest / tests_gen_bank_account

## Metrics

```json
{
  "wall_s": 12.2453,
  "ttft_s": 1.8362,
  "eval_count": 643,
  "prompt_eval_count": 293,
  "eval_duration_s": 10.4089,
  "prompt_eval_duration_s": 1.6431,
  "load_duration_s": 0.0006,
  "total_duration_s": 12.2448,
  "done_reason": "stop",
  "tokens_per_s": 61.774
}
```

## Response

````text
```python
from solution import BankAccount


def test_initial_balance_default():
    account = BankAccount()
    assert account.get_balance() == 0


def test_initial_balance_positive():
    account = BankAccount(100)
    assert account.get_balance() == 100


def test_initial_balance_negative_raises():
    try:
        BankAccount(-1)
        assert False, "Expected ValueError for negative initial balance"
    except ValueError:
        pass


def test_deposit_positive():
    account = BankAccount(50)
    account.deposit(30)
    assert account.get_balance() == 80


def test_deposit_zero_raises():
    account = BankAccount(50)
    try:
        account.deposit(0)
        assert False, "Expected ValueError for zero deposit"
    except ValueError:
        pass
    assert account.get_balance() == 50


def test_deposit_negative_raises():
    account = BankAccount(50)
    try:
        account.deposit(-10)
        assert False, "Expected ValueError for negative deposit"
    except ValueError:
        pass
    assert account.get_balance() == 50


def test_deposit_non_integer_raises():
    account = BankAccount(50)
    try:
        account.deposit(10.5)
        assert False, "Expected ValueError for non-integer deposit"
    except ValueError:
        pass
    assert account.get_balance() == 50


def test_withdraw_positive():
    account = BankAccount(100)
    account.withdraw(40)
    assert account.get_balance() == 60


def test_withdraw_zero_raises():
    account = BankAccount(100)
    try:
        account.withdraw(0)
        assert False, "Expected ValueError for zero withdrawal"
    except ValueError:
        pass
    assert account.get_balance() == 100


def test_withdraw_negative_raises():
    account = BankAccount(100)
    try:
        account.withdraw(-20)
        assert False, "Expected ValueError for negative withdrawal"
    except ValueError:
        pass
    assert account.get_balance() == 100


def test_withdraw_non_integer_raises():
    account = BankAccount(100)
    try:
        account.withdraw(20.5)
        assert False, "Expected ValueError for non-integer withdrawal"
    except ValueError:
        pass
    assert account.get_balance() == 100


def test_withdraw_exceeds_balance_raises():
    account = BankAccount(50)
    try:
        account.withdraw(100)
        assert False, "Expected ValueError for withdrawal exceeding balance"
    except ValueError:
        pass
    assert account.get_balance() == 50


def test_get_balance():
    account = BankAccount(42)
    assert account.get_balance() == 42
```
````
