import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account_card, mask_acc_card",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(account_card, mask_acc_card):
    assert mask_account_card(account_card) == mask_acc_card


@pytest.mark.parametrize(
    "date, date_form", [("2024-03-11T02:26:18.671407", "11.03.2024"), ("2019-04-15T02:26:18.671407", "15.04.2019")]
)
def test_get_date(date, date_form):
    assert get_date(date) == date_form
