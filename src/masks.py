card_number = input()

account = input()


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску."""
    card_number_str = str(card_number)
    mask_card_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
    return mask_card_number


def get_mask_account(account: str) -> str:
    """Функция, которая принимает на вход номер счета и возвращает его маску."""
    account_str = str(account)
    mask_account = f"**{account_str[-4:]}"
    return mask_account
