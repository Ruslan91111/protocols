"""
Модуль для добавления в каждую таблицу из переданных данных выводов о соответствии
результатов исследования нормам для каждого конкретного показателя и наличие нарушений
в целом для всей таблицы.

Классы:
    - ConclusionCreator:
        Класс для добавления выводов о соответствии результатов нормам для показателей.
        и общего вывода о наличии нарушений для всей таблицы.

Функции:
    - append_conclusions:
        Обработать одну таблицу, организовать сравнение, добавить выводы о
        соответствии норм для каждого показателя, и для всей таблицы в целом.

    - add_conclusions_for_all_tables:
        Добавить выводы о соответствии норм для всех таблиц.

            :param: - tables_data: dict - данные из таблиц после работы модуля file-parser.py

Пример использования:
    - add_conclusions_for_all_tables(tables_data)

"""
import re

from league_sert.data_preparation.comparator import create_conformity_conclusion
from league_sert.data_preparation.exceptions import TypeOfIndicatorTableError, NoneConformityError


class ConclusionCreator:
    """ Класс для добавления выводов о соответствии результатов нормам для показателей.
    и общего вывода о наличии нарушений для всей таблицы.
    """

    def __init__(self, table: list[list]):
        """ Конструктор:
            :param table - одна таблица, строки которой представлены в виде списков.
        """
        self.table = table  # Таблица показателей исследования
        self.row = None  # Текущая строка.
        self.value = None  # Значения для показателя для словаря
        self.type_of_table = self.determine_table_type()
        self.row_values = {}  # Набор параметров для записи в результат.
        self.result_table = {}  # Выходные данные.
        self.conformity = None

    def determine_table_type(self) -> str:
        """ Определить тип таблицы. От типа таблицы зависит как будут
        формироваться значения для последующего сравнения и записи в итог."""

        first_row = self.table[0]

        if (re.search(r"(Наименование|Показатели)", first_row[0]) and
                re.search(r"(Результат|Результат измерений)", first_row[1]) and
                re.search(r"Требования", first_row[2])):
            return 'indicators'

        if (re.search(r"(Наименование|Показатели)", first_row[1]) and
                re.search(r"(Результат|Результат измерений)", first_row[2]) and
                re.search(r"Требования", first_row[3])):
            return 'indicators_type2'

        if (re.search(r"Место отбора пробы", first_row[1]) and
                re.search(r"Наименование", first_row[2]) and
                re.search(r"Результат", first_row[3])):
            return 'indicators_air'

        if (re.search(r"Место измерений", first_row[1]) and
                re.search(r"Измеряемый параметр", first_row[2]) and
                re.search(r"Единицы", first_row[4])):
            return 'prod_control'

        if (re.search(r"(Объект смыва)", first_row[1]) and
                re.search(r"(Результат|Результат измерений)", first_row[3]) and
                re.search(r"Требования", first_row[4])):
            return 'washings'

        # Если тип таблицы с показателями не определен поднять исключение.
        raise TypeOfIndicatorTableError()

    def _update_conformity(self):
        """ Добавить в словарь вывод о соответствии нормам. """
        return ({'conformity_main': self.conformity} if isinstance(self.conformity, bool) else
                {'conformity_main': self.conformity[0],
                 'conformity_deviation': self.conformity[1]})

    def _form_indic(self):
        """ Добавить в результат строку с показателями. """
        self.value = {'result': self.row_values['result'],
                      'norm': self.row_values['norm'],
                      'norm_doc': self.row_values['norm_doc']}

    def _form_air(self):
        """ Добавить в результат строку с показателями. """
        self.value = {'name': self.row_values['name_indic'],
                      'sampling_site': self.row_values['name'],
                      'result': self.row_values['result'],
                      'norm': self.row_values['norm'],
                      'norm_doc': self.row_values['norm_doc']}

    def _form_prod_control(self):
        """ Добавить в результат строку по производственному контролю. """
        self.value = {'name': self.row_values['parameter'],
                      'unit': self.row_values['unit'],
                      'result': self.row_values['result'],
                      'norm': self.row_values['norm'],
                      'sampling_site': self.row_values['name']}

    def _form_washings(self):
        """ Добавить в результат строку по производственному контролю. """
        self.value = {'result': self.row_values['result'],
                      'norm': self.row_values['norm'],
                      'norm_doc_of_method': self.row_values['norm_doc_of_method']}

    def append_row(self):
        """ Добавить строку в результат. Логика обработки и структура строки определяется
         в зависимости от типа таблицы."""
        methods = {'indicators': self._form_indic,
                   'indicators_type2': self._form_indic,
                   'prod_control': self._form_prod_control,
                   'indicators_air': self._form_air,
                   'washings': self._form_washings}

        method_of_form_value = methods.get(self.type_of_table, None)
        method_of_form_value()
        self.value.update(self._update_conformity())
        self.save_key_in_result()

    def save_key_in_result(self):
        """ Сохранить ключ - показатель. В процессе проверить наличие ключа в результате,
        если ключ уже имеется добавить цифру в конце ключа."""

        # Если такой ключ уже есть.
        if self.result_table.get(self.row_values['name'], False):
            # Подставляем цифру в ключ
            for i in range(50):
                # Если ключ с цифрой тоже есть
                if self.result_table.get(self.row_values['name'] + str(i), False):
                    continue
                # Если ключа с цифрой нет, то сохраняем
                self.result_table[self.row_values['name'] + "_" + str(i)] = self.value
                break
        else:
            self.result_table[self.row_values['name']] = self.value

    def check_valid_row(self):
        """ Проверить валидная ли строка. """
        if len(set(self.row)) == 1:
            return False
        return True

    def determine_params(self):
        """ Определить набор параметров для сравнения и последующей записи. """
        if self.type_of_table == 'indicators':
            self.row_values = {'name': self.row[0],
                               'result': self.row[1],
                               'norm': self.row[2],
                               'norm_doc': self.row[3]}

        if self.type_of_table == 'indicators_type2':
            self.row_values = {'name': self.row[1],
                               'result': self.row[2],
                               'norm': self.row[3],
                               'norm_doc': self.row[4]}

        elif self.type_of_table == 'prod_control':
            self.row_values = {'name': self.row[1],
                               'parameter': self.row[2] + ' ' + self.row[3],
                               'unit': self.row[4],
                               'result': self.row[5],
                               'norm': self.row[6]}

        elif self.type_of_table == 'indicators_air':
            self.row_values = {'name': self.row[1],
                               'name_indic': self.row[2],
                               'result': self.row[3], 'norm': self.row[4],
                               'norm_doc': self.row[5]}

        elif self.type_of_table == 'washings':
            self.row_values = {'washings_object': self.row[1],
                               'name': self.row[2],
                               'result': self.row[3],
                               'norm': self.row[4],
                               'norm_doc_of_method': self.row[4]}

    def make_conformity(self):
        """ Сделать выводы о соответствии показателей и норм. """
        self.conformity: bool | tuple[bool] = create_conformity_conclusion(
            self.row_values['result'], self.row_values['norm'])

        if self.conformity is None:
            raise NoneConformityError(self.row_values['result'], self.row_values['norm'])

    def append_conclusions(self):
        """ Добавить выводы о соответствии показателей нормам в таблицу. """
        for row in self.table[1:]:
            self.row = row
            if not self.check_valid_row():
                continue
            self.determine_params()
            self.make_conformity()
            self.append_row()


def append_conclusions(indicators: list[list]) -> dict | None:
    """ Функция для добавления выводов о соответствии нормам в таблицу"""
    conclusions = ConclusionCreator(indicators)
    conclusions.append_conclusions()
    return conclusions.result_table


def add_conclusions_for_all_tables(tables_data: dict) -> dict:
    """ Добавить выводы о соответствии норм для всех таблиц. """
    for key, value in tables_data.items():
        if key[1] not in {'RESULTS', 'PROD_CONTROL'}:
            continue
        tables_data[key] = append_conclusions(value)
    return tables_data
