from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """Функция, которая принимает на вход номер карты и возвращает ее маску."""
    # Приводим входное значение к строке
    if account_card is None:
        return "Счёт/карта не указаны"

    account_str = str(account_card).strip()

    # Обрабатываем пустые строки
    if not account_str:
        return "Счёт/карта не указаны"

    parts = account_str.split()

    # Если нет разделения на тип и номер (например, просто число)
    if len(parts) < 2:
        number = account_str
        # Определяем тип по длине номера
        if len(number) >= 16:
            return get_mask_card_number(number)
        else:
            return get_mask_account(number)

    # Есть разделение на тип и номер
    name_part = " ".join(parts[:-1])
    number = parts[-1]

    # Нормализуем тип счёта/карты (без учёта регистра)
    name_lower = name_part.lower()

    if "счет" in name_lower or "account" in name_lower:
        number_card_mask = get_mask_account(number)
    else:
        number_card_mask = get_mask_card_number(number)

    return f"{name_part} {number_card_mask}"


def get_date(date: str) -> str:
    """Функция,которая принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    return f"{date[8:10]}.{date[5:7]}.{date[:4]}"
