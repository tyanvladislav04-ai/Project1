import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

PATH_TO_FILE = os.path.join(ROOT_DIR, "operations.json")


def bank_operations(PATH_TO_FILE) -> list:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых
    транзакциях"""
    try:
        with open(PATH_TO_FILE, "r", encoding="utf-8") as file:
            operations = json.load(file)
            if isinstance(operations, list):
                return operations
    except (FileNotFoundError, json.JSONDecodeError):
        return []
