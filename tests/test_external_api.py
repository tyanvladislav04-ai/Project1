from unittest.mock import patch

from src.external_api import transaction_amount


@patch("requests.get")
def test_transaction_amount(mock_get):
    mock_get.return_value.json.return_value = {
        "id": 587085106,
        "state": "EXECUTED",
        "date": "2018-03-23T10:45:06.972075",
        "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Открытие вклада",
        "to": "Счет 41421565395219882431",
    }
    assert (
        transaction_amount(
            {
                "id": 587085106,
                "state": "EXECUTED",
                "date": "2018-03-23T10:45:06.972075",
                "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            }
        )
        == 48223.05
    )


def test_transaction_amount_missing_currency():
    transaction = {"operationAmount": {"amount": "100.00"}}
    try:
        transaction_amount(transaction)
        assert False, "Ожидалась ошибка KeyError"
    except KeyError:
        pass


def test_transaction_amount_rub_only():
    transaction = {"operationAmount": {"amount": "2000.50", "currency": {"code": "RUB"}}}
    result = transaction_amount(transaction)
    assert result == 2000.5


@patch("requests.get")
@patch("os.getenv")
def test_transaction_amount_usd_conversion(mock_os_getenv, mock_get):
    mock_os_getenv.return_value = "test_api_key_123"
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"info": {"rate": 71.0}, "result": 697508.97}  # 1 USD = 71 RUB  # 9824.07 * 71.0
    transaction_data = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }
    result = transaction_amount(transaction_data)
    expected = 9824.07 * 71.0
    assert abs(result - expected) < 0.01
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "test_api_key_123"},
        params={"to": "RUB", "from": "USD", "amount": "9824.07"},
    )
