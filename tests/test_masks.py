from src.masks import get_mask_account, get_mask_card_number
import pytest


@pytest.mark.parametrize(
    "account, mask_account",
    [("73654108430135874305", "**4305"), ("", "**"), ("123456", "**3456"), ("12345678901234567890", "**7890")],
)
def test_get_mask_account(account, mask_account):
    assert get_mask_account(account) == mask_account


@pytest.mark.parametrize(
    "card_number, mask_card_number",
    [("7000792289606361", "7000 79** **** 6361"), ("", " ** **** "), ("12345678901234567890", "1234 56** **** 7890")],
)
def test_get_mask_card_number(card_number, mask_card_number):
    assert get_mask_card_number(card_number) == mask_card_number
