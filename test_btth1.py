import pytest
import btth1


def setup_function():
    btth1.balance = 0


def test_deposit_success():

    btth1.deposit(100000)

    assert btth1.balance == 100000


def test_transfer_insufficient_balance():

    with pytest.raises(
        btth1.InsufficientBalanceError
    ):
        btth1.transfer(
            "0987654321",
            100000
        )


def test_invalid_amount():

    with pytest.raises(
        btth1.InvalidAmountError
    ):
        btth1.deposit(-1000)