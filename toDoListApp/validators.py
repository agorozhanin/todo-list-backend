# Файл с функциями проверки на корректность данных атрибутов сущности
import re


# Проверка на корректность статуса задачи
def is_status(status):
    if isinstance(status, bool) or status in ('True', 'False'):
        return True
    return False


# Проверка на корректность названия задачи
def is_correct_name(name):
    if re.fullmatch('\s+', name) is None and name != '':
        return True
    return False
