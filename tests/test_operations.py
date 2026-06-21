import unittest
from unittest.mock import Mock, patch

from src.operations import process_bank_operations, process_bank_search


class TestProcessBankSearch(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_data = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Открытие вклада"},
            {"id": 3, "description": "Перевод со счета на счет"},
            {"id": 4, "description": "Перевод с карты на карту"},
            {"id": 5, "description": "Перевод с карты на счет"},
        ]

    @patch("re.compile")
    def test_no_matches(self, mock_compile):
        """Тест поиска без совпадений."""
        mock_pattern = Mock()
        mock_pattern.search.return_value = None  # Нет совпадений
        mock_compile.return_value = mock_pattern

        result = process_bank_search(self.test_data, "не существующее слово")

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    @patch("re.compile")
    def test_basic_search(self, mock_compile):
        """Тест базового поиска по подстроке."""
        mock_pattern = Mock()
        mock_pattern.search.return_value = True
        mock_compile.return_value = mock_pattern

        result = process_bank_search(self.test_data, "организации")

        mock_compile.assert_called_once_with("организации")
        self.assertEqual(len(result), 5)

    @patch("re.compile")
    def test_empty_data(self, mock_compile):
        """Тест с пустыми данными."""
        mock_pattern = Mock()
        mock_pattern.search.return_value = True
        mock_compile.return_value = mock_pattern

        result = process_bank_search([], "организации")

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])


class TestProcessBankOperations(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_data_1 = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Открытие вклада"},
            {"id": 3, "description": "Перевод со счета на счет"},
            {"id": 4, "description": "Перевод с карты на карту"},
            {"id": 5, "description": "Перевод с карты на счет"},
        ]
        self.categories = [
            "Перевод организации",
            "Открытие вклада",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод с карты на счет",
        ]

    def test_empty_data(self):
        """Тест с пустыми данными"""
        result = process_bank_operations([], ["Перевод организации", "Открытие вклада"])
        expected = {"Перевод организации": 0, "Открытие вклада": 0}
        self.assertEqual(result, expected)

    @patch("collections.Counter")
    def test_duplicate_operations(self, mock_counter):
        """Тест повторяющихся операций."""
        duplicate_data = [
            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Перевод организации"},
            {"id": 3, "description": "Открытие вклада"},
        ]

        mock_counter_instance = Mock()
        mock_counter_instance.get.side_effect = lambda key, default: {
            "Перевод организации": 2,
            "Открытие вклада": 1,
        }.get(key, default)
        mock_counter.return_value = mock_counter_instance

        categories = ["Перевод организации", "Открытие вклада"]
        result = process_bank_operations(duplicate_data, categories)

        expected = {"Перевод организации": 2, "Открытие вклада": 1}
        self.assertEqual(result, expected)
