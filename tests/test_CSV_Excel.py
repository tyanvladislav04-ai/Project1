import unittest
from unittest.mock import mock_open, patch

import pandas as pd

from src.CSV_Excel import func_csv, funs_excel


class TestFuncCsv(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="invalid csv content")
    def test_csv_decode_error(self, mock_file):
        result = func_csv("invalid.csv")

        self.assertIsInstance(result, list)
        self.assertEqual(result, [])

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            "id;state;date;amount;currency_name;currency_code;from;to;description\n"
            "650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;"
            "Счет 39745660563456619397;Перевод организации"
        ),
    )
    def test_valid_csv_single_transaction(self, mock_file):
        result = func_csv("single.csv")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

        transaction = result[0]
        expected_transaction = {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": "16210",
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        }
        self.assertEqual(transaction, expected_transaction)
        mock_file.assert_called_once_with("single.csv", "r", encoding="utf-8")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="id;state;date;amount;currency_name;currency_code;from;to;description\n",
    )
    def test_empty_csv_only_headers(self, mock_file):
        result = func_csv("empty.csv")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        mock_file.assert_called_once_with("empty.csv", "r", encoding="utf-8")


class TestFuncExcel(unittest.TestCase):
    @patch("pandas.read_excel")
    def test_valid_excel_multiple_transactions(self, mock_read_excel):
        test_data = pd.DataFrame(
            {
                "id": ["650703", "650704"],
                "state": ["EXECUTED", "EXECUTED"],
                "amount": ["16210", "5000"],
                "currency_name": ["Sol", "Ruble"],
                "description": ["Перевод организации", "Перевод клиенту"],
            }
        )
        mock_read_excel.return_value = test_data

        result = funs_excel("test.xlsx")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "650703")
        self.assertEqual(result[1]["state"], "EXECUTED")
        mock_read_excel.assert_called_once_with("test.xlsx")

    @patch("pandas.read_excel", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_read_excel):
        result = funs_excel("nonexistent.xlsx")

        self.assertIsInstance(result, list)
        self.assertEqual(result, [])
        mock_read_excel.assert_called_once_with("nonexistent.xlsx")

    @patch("pandas.read_excel", side_effect=pd.errors.EmptyDataError())
    def test_empty_excel_file(self, mock_read_excel):
        result = funs_excel("empty.xlsx")

        self.assertIsInstance(result, list)

        self.assertEqual(result, [])
        mock_read_excel.assert_called_once_with("empty.xlsx")
