import os
from typing import Dict

import requests
from dotenv import load_dotenv


def transaction_amount(transaction: Dict) -> float:
    """функцию, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных —
    float. Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют и
    конвертации суммы операции в рубли"""
    amount_transact = transaction["operationAmount"]["amount"]
    currency_transact = transaction["operationAmount"]["currency"]["code"]
    rub_amount = 0
    if currency_transact == "RUB":
        rub_amount += float(amount_transact)
    elif currency_transact == "USD" or currency_transact == "EUR":
        load_dotenv()
        api_key = os.getenv("API_KEY")
        url = "https://api.apilayer.com/exchangerates_data/convert"
        headers = {"apikey": api_key}
        params = {"to": "RUB", "from": currency_transact, "amount": amount_transact}
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        rates = result.get("info", {}).get("rate")
        result_rub = float(rates) * float(amount_transact)
        rub_amount = +float(result_rub)
    return rub_amount
