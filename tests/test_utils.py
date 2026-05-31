import unittest
from unittest.mock import mock_open, patch

from src.utils import bank_operations


class TestBankOperations(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
    def test_valid_json(self, mock_file):
        result = bank_operations("test.json")
        self.assertEqual(result, [{"id": 1}])
        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_invalid_json(self, mock_file):
        result = bank_operations("test.json")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_file):
        result = bank_operations("test.json")
        self.assertEqual(result, [])
        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")
