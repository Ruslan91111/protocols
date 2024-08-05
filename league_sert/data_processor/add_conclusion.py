""" Перебрать таблицы, добавить выводы о соответствии


Функции:
    - is_indicators:
        Проверка, что таблица относится к Показателям.

    - append_conclusions:
        Обработать одну таблицу, организовать сравнение, добавить выводы о
        соответствии норм для каждого показателя, и для всей таблицы в целом.

    - add_conclusions_for_all_tables:
        Добавить выводы о соответствии норм для всех таблиц.

"""
import re

from league_sert.data_processor.comparator import create_conformity_conclusion
from league_sert.data_processor.file_data_collector import MainCollector, FILE, FILE2


def is_indicators(first_row) -> bool:
    """ Проверка, что таблица относится к Показателям. """
    if (re.search(r"(Наименование|Показатели)", first_row[0]) and
            re.search(r"(Результат|Результат измерений)", first_row[1]) and
            re.search(r"Требования", first_row[2])):
        return True


def append_conclusions(indicators: list[list]) -> dict | None:
    """ Добавить выводы о соответствии нормам в данные из одной таблицы.
     Принимает на вход список, списков, каждый внутренний список - это данные
     из одной строки таблицы. Далее результат исследования и норма передаются
     во внешнюю функцию, которая возвращает в виде bool | tuple[bool]
     вывод о соответствии показателей. Все полученные данные записываются в словарь.
     Где ключ- 'наименование показателя', значение - все остальные значения.
     Также в итоговом словаре записывается вывод о наличии нарушений в таблице. """

    if not is_indicators(indicators[0]):
        return None

    violation_main_digit = False  # Наличие нарушений во всей таблице для основных показателей.
    violation_digit_with_dev = False  # для показателей с отклонением.
    indic_result = {}  # Обработанные индикаторы.

    # Цикл по строкам в таблице. Строка - список.
    for row in indicators[1:]:
        if len(set(row)) == 1:
            continue

        # Значения из текущей строки.
        name, result, norm, norm_doc = row
        # Получаем вывод о соответствии по конкретной строке.
        conformity: bool | tuple[bool] = create_conformity_conclusion(result, norm)

        # Работа с переменными нарушений для всей таблицы.
        if isinstance(conformity, bool) and not conformity and violation_main_digit is False:
            violation_main_digit = True
        elif isinstance(conformity, tuple):
            if not conformity[0]:
                violation_main_digit = True
            if not conformity[1]:
                violation_digit_with_dev = True

        # Записать таблицу в результат, где ключ - наименование показателя.
        indic_result[name] = {
            'result': result, 'norm': norm, 'norm_doc': norm_doc,
            **({'conformity_main': conformity} if isinstance(conformity, bool) else
               {'conformity_main': conformity[0], 'conformity_deviation': conformity[1]})}

    # Записать вывод о наличии нарушений для все таблицы.
    indic_result['violations_of_norms'] = (violation_main_digit, violation_digit_with_dev)
    return indic_result


def add_conclusions_for_all_tables(tables_data):
    """ Добавить выводы о соответствии норм для всех таблиц. """
    for key, value in tables_data.items():
        if key[1] != 'RESULTS':
            continue
        tables_data[key] = append_conclusions(value)
    return tables_data


def main():
    data_getter = MainCollector(FILE2)
    data_getter.collect_all_data()
    add_conclusions_for_all_tables(data_getter.data_from_tables)
    print(data_getter.data_from_tables)


if __name__ == '__main__':
    main()
