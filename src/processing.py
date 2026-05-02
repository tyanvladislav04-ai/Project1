filter_by_state_list = input()

def filter_by_state(filter_by_state_list: list, state='EXECUTED') -> list:
    """Функция, filter_by_state, которая принимает список словарей и опционально значение для ключа
state (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
state соответствует указанному значению"""
    result_list = []
    for dict_state in filter_by_state_list:
        if dict_state['state'] == state:
            result_list.append(dict_state)
    return result_list

def sort_by_date(filter_by_state_list, descending: bool = True) -> list:
    """Функция, sort_by_date, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание). Функция должна возвращать новый список,
    отсортированный по дате (date)"""
    sorted_list = sorted(filter_by_state_list, key=lambda employee: employee['date'], reverse=True)
    return sorted_list









