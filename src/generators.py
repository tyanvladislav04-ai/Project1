from typing import List, Dict, Any, Iterator, Generator


def filter_by_currency(transactions: List[dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """Функция, filter_by_currency, которая принимает на вход список словарей, представляющих транзакции.
    Функция возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной
    (например, USD)"""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction
        else:
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str]:
    """Генератор transaction_descriptions, который принимает список словарей с транзакциями и возвращает описание
    каждой операции по очереди"""
    for transaction in transactions:
        description = transaction.get("description")
        yield description


def card_number_generator(start: int, end: int) -> Generator[str]:
    """Генератор card_number_generator, который выдает номера банковских карт в формате
    XXXX XXXX XXXX XXXX, где X — цифра номера карты. Генератор может сгенерировать номера карт в заданном диапазоне
    от 0000 0000 0000 0001 до 9999 9999 9999 9999"""
    if not (1 <= start <= 9999999999999999):
        raise ValueError("Начальное значение должно быть от 1 до 9999999999999999")
    if not (1 <= end <= 9999999999999999):
        raise ValueError("Конечное значение должно быть от 1 до 9999999999999999")
    if start > end:
        raise ValueError("Начальное значение должно быть меньше конечного")
    for number in range(start, end + 1):
        formatted = f"{number:016d}"
        card_number = " ".join(formatted[i : i + 4] for i in range(0, 16, 4))
        yield card_number
