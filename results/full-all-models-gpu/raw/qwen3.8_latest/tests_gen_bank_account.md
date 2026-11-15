# qwen3.8:latest / tests_gen_bank_account

## Metrics

```json
{
  "wall_s": 22.6463,
  "ttft_s": 2.0275,
  "eval_count": 686,
  "prompt_eval_count": 291,
  "eval_duration_s": 20.6189,
  "prompt_eval_duration_s": 1.8091,
  "load_duration_s": 0.0006,
  "total_duration_s": 22.6457,
  "done_reason": "stop",
  "tokens_per_s": 33.27
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
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_deposit_positive():
    account = BankAccount(0)
    account.deposit(50)
    assert account.get_balance() == 50


def test_deposit_zero_raises():
    account = BankAccount(10)
    try:
        account.deposit(0)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    assert account.get_balance() == 10


def test_deposit_negative_raises():
    account = BankAccount(10)
    try:
        account.deposit(-5)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    assert account.get_balance() == 10


def test_deposit_non_integer_raises():
    account = BankAccount(10)
    try:
        account.deposit(5.5)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    assert account.get_balance() == 10


def test_withdraw_positive():
    account = BankAccount(100)
    account.withdraw(30)
    assert account.get_balance() == 70


def test_withdraw_zero_raises():
    account = BankAccount(10)
    try:
        account.withdraw(0)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    assert account.get_balance() == 10


def test_withdraw_negative_raises():
    account = BankAccount(10)
    try:
        account.withdraw(-5)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    assert account.get_balance() == 10


def test_withdraw_non_integer_raises():
    account = BankAccount(10)
    try:
        account.withdraw(5.5)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    assert account.get_balance() == 10


def test_withdraw_exceeds_balance_raises():
    account = BankAccount(10)
    try:
        account.withdraw(20)
        assert False, "Expected ValueError"
    except ValueError:
        pass
    assert account.get_balance() == 10


def test_withdraw_exact_balance():
    account = BankAccount(10)
    account.withdraw(10)
    assert account.get_balance() == 0


def test_multiple_operations():
    account = BankAccount(50)
    account.deposit(25)
    account.withdraw(10)
    account.deposit(5)
    account.withdraw(30)
    assert account.get_balance() == 40
```
````
