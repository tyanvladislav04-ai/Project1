import csv
import json
import os
from typing import Any, Dict, List

import pandas as pd

from src.CSV_Excel import func_csv, funs_excel
from src.operations import process_bank_search
from src.processing import filter_by_state, sort_by_date
from src.utils import bank_operations
from src.widget import get_date, mask_account_card


def main() -> List[Dict[str, Any]]:
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON‑файла\n"
        "2. Получить информацию о транзакциях из CSV‑файла\n"
        "3. Получить информацию о транзакциях из XLSX‑файла\n"
    )

    while True:
        user_input_1 = input("\nВведите номер пункта (1–3): ").strip()

        if user_input_1 not in ("1", "2", "3"):
            print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3")
            continue

        # Выбор файла и загрузка данных
        if user_input_1 == "1":
            print("Для обработки выбран JSON‑файл")
            ROOT_DIR = os.path.dirname(__file__)
            PATH_TO_FILE = os.path.join(ROOT_DIR, "operations.json")
            operations = bank_operations(PATH_TO_FILE)
        elif user_input_1 == "2":
            print("Для обработки выбран CSV‑файл")
            ROOT_DIR = os.path.dirname(__file__)
            transactions_csv_file = os.path.join(ROOT_DIR, "transactions.csv")
            operations = func_csv(transactions_csv_file)
        else:  # user_input_1 == '3'
            print("Для обработки выбран XLSX‑файл")
            ROOT_DIR = os.path.dirname(__file__)
            transactions_excel_file = os.path.join(ROOT_DIR, "transactions_excel.xlsx")
            operations = funs_excel(transactions_excel_file)

        # Проверка загрузки данных
        if not operations:
            print("Не удалось загрузить транзакции. Проверьте файл и повторите попытку.")
            continue

        # Фильтрация по статусу
        valid_states = {"EXECUTED", "CANCELED", "PENDING"}
        user_input_2 = None
        while user_input_2 not in valid_states:
            print(
                "Введите статус, по которому необходимо выполнить фильтрацию. "
                "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
            )
            user_input_2 = input().strip().upper()
            if user_input_2 not in valid_states:
                print(f"Статус операции '{user_input_2}' недоступен.")
        filtered_operations = filter_by_state(operations, user_input_2)

        # Сортировка по дате
        print("\nОтсортировать операции по дате? (Да/Нет)")
        sort_choice = input().strip().lower()
        if sort_choice == "да":
            print("Отсортировать по возрастанию или по убыванию? (По возрастанию/ По убыванию)")
            order_choice = input().strip().lower()
            descending = order_choice == "по убыванию"
            filtered_operations = sort_by_date(filtered_operations, descending=descending)

        # Фильтрация по рублёвым транзакциям
        print("\nВыводить только рублёвые транзакции? (Да/Нет)")
        rub_choice = input().strip().lower()
        if rub_choice == "да":
            filtered_operations = [
                op
                for op in filtered_operations
                if op.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
            ]

        # Поиск по описанию
        print("\nОтфильтровать список транзакций по определённому слову в описании? (Да/Нет)")
        search_choice = input().strip().lower()
        if search_choice == "да":
            print("Введите слово для поиска:")
            search_word = input().strip()
            filtered_operations = process_bank_search(filtered_operations, search_word)

        # Вывод результатов в требуемом формате
        print("\nРаспечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(filtered_operations)}")
        print()  # Пустая строка для разделения

        for op in filtered_operations:
            # 1. Дата и описание
            date_str = op.get("date", "")
            description = op.get("description", "Описание отсутствует")

            if date_str:
                formatted_date = get_date(date_str)
                print(f"{formatted_date} {description}")
            else:
                print(description)

            # 2. Обработка счетов и карт
            from_account = op.get("from", "")
            to_account = op.get("to", "")

            if from_account and to_account:
                # Перевод между счетами/картами
                masked_from = mask_account_card(from_account)
                masked_to = mask_account_card(to_account)
                print(f"{masked_from} -> {masked_to}")
            elif from_account:
                # Исходящий перевод (только источник)
                masked_from = mask_account_card(from_account)
                print(masked_from)
            elif to_account:
                # Входящий перевод (только получатель)
                masked_to = mask_account_card(to_account)
                print(masked_to)

            # 3. Сумма
            # Пытаемся получить сумму из разных возможных источников
            amount_raw = None
            currency_code = "RUB"

            # Вариант 1: ищем в operationAmount (для JSON)
            operation_amount = op.get("operationAmount", {})
            if operation_amount:
                amount_raw = operation_amount.get("amount")
                currency_info = operation_amount.get("currency", {})
                currency_code = currency_info.get("code", "RUB")

            # Вариант 2: ищем на верхнем уровне (для CSV/Excel)
            if amount_raw is None:
                amount_raw = op.get("amount")
            if currency_code == "RUB":  # если не нашли в operationAmount
                currency_code = op.get("currency_code", "RUB")

            # Обрабатываем пустые/некорректные значения
            if pd.isna(amount_raw) or amount_raw is None:
                amount_float = 0.0
            else:
                try:
                    # Преобразуем строку в число, заменяя запятые на точки
                    amount_str = str(amount_raw).replace(",", ".")
                    amount_float = float(amount_str)
                except (ValueError, TypeError) as ex:
                    amount_float = 0.0

            # Форматирование суммы
            if currency_code == "RUB":
                amount_str = f"{amount_float:.0f} руб."
            else:
                amount_str = f"{amount_float} {currency_code}"

            print(f"Сумма: {amount_str}")

            print()  # Пустая строка между операциями

        break
    return filtered_operations


if __name__ == "__main__":
    main()
