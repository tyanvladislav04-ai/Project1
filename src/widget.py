from masks import get_mask_account, get_mask_card_number

account_card = input()
date = input()


def mask_account_card(account_card: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску."""
    account_card_split = account_card.split()
    name_card = " ".join(account_card_split[:-1])
    number_card = str(account_card_split[-1])
    if name_card == "Счет" and "счет":
        number_card_mask = get_mask_card_number(number_card)
    else:
        number_card_mask = get_mask_account(number_card)

    return f"{name_card} {number_card_mask}"


def get_date(date: str) -> str:
    """Функция,которая принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
