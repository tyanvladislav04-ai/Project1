import pytest

from src.decorators import log


def test_log_1(capsys):
    @log()
    def test_function(x, y):
        return x + y

    result = test_function(5, 3)
    captured = capsys.readouterr()
    assert result == 8
    assert "test_function ok" in captured.out


def test_log_2(capsys):
    @log()
    def test_function(x, y):
        return x + y

    result = test_function(1, 3)
    captured = capsys.readouterr()
    assert result == 4
    assert "test_function ok" in captured.out


def test_log_error(capsys):
    @log()
    def test_function(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        test_function(5, 0)
    captured = capsys.readouterr()
    assert "test_function error: division by zero" in captured.out
    assert "Inputs: args=(5, 0)" in captured.out
