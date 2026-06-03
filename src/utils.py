import json
import os
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

PATH_TO_FILE = os.path.join(ROOT_DIR, "operations.json")

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs/utils.log"), "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def bank_operations(PATH_TO_FILE) -> list:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых
    транзакциях"""
    try:
        with open(PATH_TO_FILE, "r", encoding="utf-8") as file:
            operations = json.load(file)
            logger.info(f"Попытка загрузить транзакции из файла: {PATH_TO_FILE}")
            if isinstance(operations, list):
                logger.info("Данные успешно загружены.")
                return operations
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        logger.error(f"Неожиданная ошибка при загрузке файла {PATH_TO_FILE}: {ex}")
        return []
