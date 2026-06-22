import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Функция, которая принимает список словарей с данными о банковских операциях и строку поиска, а возвращает список
    словарей, у которых в описании есть данная строка"""
    pattern = re.compile(search, re.IGNORECASE)
    return [item for item in data if pattern.search(str(item.get("description", "")))]


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Функция, которая принимает список словарей с данными о банковских операциях и список категорий операций, а
    возвращает словарь, в котором ключи — это названия категорий, а значения — это количество операций
    в каждой категории"""
    descriptions = [op.get("description", "") for op in data]
    counts = Counter(descriptions)
    result = {}
    for category in categories:
        result[category] = counts.get(category, 0)
    return result
