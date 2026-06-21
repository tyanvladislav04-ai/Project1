import os
from typing import Any, Dict, List

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
        user_input_1 = input("\nВведите номер пункта (1–4): ").strip()

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
            rub_operations = []
            for op in filtered_operations:
                currency = op.get("operationAmount", {}).get("currency", {}).get("code")
                if currency == "RUB":
                    rub_operations.append(op)

            filtered_operations = rub_operations

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

            if from_account:
                masked_from = mask_account_card(from_account)
                print(masked_from)
            if to_account:
                masked_to = mask_account_card(to_account)
                print(masked_to)

            # 3. Сумма
            amount = op.get("operationAmount", {}).get("amount", "0")
            currency_code = op.get("operationAmount", {}).get("currency", {}).get("code", "RUB")
            if currency_code == "RUB":
                amount_str = f"{float(amount):.0f} руб."
            else:
                amount_str = f"{float(amount)} {currency_code}"
            print(f"Сумма: {amount_str}")


            print()  # Пустая строка между операциями

    return filtered_operations


print(main())
