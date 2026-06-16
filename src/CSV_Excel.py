import csv
import os

import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
transactions_csv_file = os.path.join(ROOT_DIR, "transactions.csv")
transactions_excel_file = os.path.join(ROOT_DIR, "transactions_excel.xlsx")


def func_csv(transactions_csv_file) -> list:
    """Функция для считывания финансовых операций из CSV выдает список словарей с транзакциями"""
    try:
        transactions = []
        with open(transactions_csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                transactions.append(row)
        return transactions
    except (FileNotFoundError, ValueError, UnicodeDecodeError):
        return []


def funs_excel(transactions_excel_file) -> list:
    """Функция для считывания финансовых операций из Excel выдает список словарей с транзакциями"""
    try:
        excel_data = pd.read_excel(transactions_excel_file)
        transactions = excel_data.to_dict(orient="records")
        return transactions
    except (FileNotFoundError, ValueError, UnicodeDecodeError):
        return []
