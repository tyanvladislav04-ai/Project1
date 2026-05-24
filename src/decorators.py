from functools import wraps


def log(filename=None) -> None:
    """Декоратор , который автоматически логирует начало и конец выполнения функции, а также ее результаты или
    возникшие ошибки. Декоратор принимает необязательный аргумент filename , который определяет, куда будут
    записываться логи в файл или в консоль)"""

    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            try:
                result = func(*args, **kwargs)
                message = f"{func_name} ok"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(message + "\n")
                else:
                    print(message)
                return result
            except Exception as e:
                error_message = f"{func_name} error: {e}. " f"Inputs: args={args}, kwargs={kwargs}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + "\n")
                else:
                    print(error_message)
                raise

        return wrapper

    return my_decorator
