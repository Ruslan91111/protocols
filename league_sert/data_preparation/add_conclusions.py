"""
Модуль для добавления в каждую таблицу из переданных данных выводов о соответствии
результатов исследования нормам для каждого конкретного показателя.

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

"""
import re

from league_sert.data_preparation.comparator import create_conformity_conclusion


class ConclusionCreator:
    """ Класс для добавления выводов о соответствии результатов нормам для показателей.
    и общего вывода о наличии нарушений для всей таблицы. """
    def __init__(self, table: list[list]):
        self.table = table  # Таблица показателей исследования
        self.violation_main_digit = False  # Нарушения во всей таблице для основных показателей.
        self.violation_digit_with_dev = False  # для показателей с отклонением.
        self.row = None  # Текущая строка.
        self.type_of_table = self.determine_table_type()
        self.row_values = {}  # Набор параметров для записи в результат.
        self.result_table = {}  # Выходные данные.
        self.conformity = None

    def determine_table_type(self) -> str:
        """ Определить тип таблицы. """

        first_row = self.table[0]

        if (re.search(r"(Наименование|Показатели)", first_row[0]) and
                re.search(r"(Результат|Результат измерений)", first_row[1]) and
                re.search(r"Требования", first_row[2])):
            return 'indicators'

        if (re.search(r"Место отбора пробы", first_row[1]) and
                re.search(r"Наименование", first_row[2]) and
                re.search(r"Результат", first_row[3])):
            return 'indicators_air'

        if (re.search(r"Место измерений", first_row[1]) and
                re.search(r"Измеряемый параметр", first_row[2]) and
                re.search(r"Единицы", first_row[4])):
            return 'prod_control'

        print('Не определен тип таблицы')

    def _row_indicator(self):
        """ Добавить в результат строку с показателями. """
        self.result_table[self.row_values['name']] = {
            'result': self.row_values['result'],
            'norm': self.row_values['norm'],
            'norm_doc': self.row_values['norm_doc'],
            **({'conformity_main': self.conformity} if isinstance(self.conformity, bool) else
               {'conformity_main': self.conformity[0],
                'conformity_deviation': self.conformity[1]})}

    def _row_indicator_air(self):
        """ Добавить в результат строку по показателям воздух. """
        self.result_table[self.row_values['number']] = {
            'place_meas': self.row_values['place_meas'],
            'name_indic': self.row_values['name_indic'],
            'result': self.row_values['result'],
            'norm': self.row_values['norm'],
            'norm_doc': self.row_values['norm_doc'],
            ** ({'conformity_main': self.conformity} if isinstance(self.conformity, bool) else
                {'conformity_main': self.conformity[0],
                 'conformity_deviation': self.conformity[1]})}

    def _row_prod_control(self):
        """ Добавить в результат строку по производственному контролю. """
        self.result_table[self.row_values['number']] = {
            'place_meas': self.row_values['place_meas'],
            'parameter': self.row_values['parameter'],
            'unit': self.row_values['unit'],
            'result': self.row_values['result'],
            'norm': self.row_values['norm'],
            **({'conformity_main': self.conformity} if isinstance(self.conformity, bool) else
               {'conformity_main': self.conformity[0],
                'conformity_deviation': self.conformity[1]})}

    def append_row(self):
        """ Добавить строку в результат в зависимости от типа таблицы."""
        if self.type_of_table == 'indicators':
            self._row_indicator()

        if self.type_of_table == 'prod_control':
            self._row_prod_control()

        if self.type_of_table == 'indicators_air':
            self._row_indicator_air()

    def check_valid_row(self):
        """ Проверить валидная ли строка. """
        if len(set(self.row)) == 1:
            return False
        return True

    def determine_params(self):
        """ Определить набор параметров для сравнения и последующей записи. """
        if self.type_of_table == 'indicators':
            self.row_values = {'name': self.row[0], 'result': self.row[1],
                               'norm': self.row[2], 'norm_doc': self.row[3]}

        elif self.type_of_table == 'prod_control':
            self.row_values = {'number': self.row[0], 'place_meas': self.row[1],
                               'parameter': self.row[2] + self.row[3],
                               'unit': self.row[4], 'result': self.row[5],
                               'norm': self.row[6]}

        elif self.type_of_table == 'indicators_air':
            self.row_values = {'number': self.row[0], 'place_meas': self.row[1],
                               'name_indic': self.row[2],
                               'result': self.row[3], 'norm': self.row[4],
                               'norm_doc': self.row[5]}

    def make_conformity(self):
        """ Сделать выводы о соответствии показателей и норм. """
        self.conformity: bool | tuple[bool] = create_conformity_conclusion(
            self.row_values['result'], self.row_values['norm'])

    def check_violations_for_table(self):
        """ Сделать и добавить в результат вывод о соответствии нормам для всей таблицы."""
        if (isinstance(self.conformity, bool) and not self.conformity
                and self.violation_main_digit is False):
            self.violation_main_digit = True

        elif isinstance(self.conformity, tuple):
            if not self.conformity[0]:
                self.violation_main_digit = True
            if not self.conformity[1]:
                self.violation_digit_with_dev = True

    def write_violations_for_table(self):
        """ Записать в словарь с таблицей вывод о наличии нарушений норм. """
        self.result_table['violations_of_norms'] = (self.violation_main_digit,
                                                    self.violation_digit_with_dev)

    def append_conclusions(self):
        """ Добавить выводы о соответствии показателей нормам в таблицу. """
        for row in self.table[1:]:
            self.row = row
            if not self.check_valid_row():
                continue

            self.determine_params()
            self.make_conformity()
            self.check_violations_for_table()
            self.append_row()

        self.write_violations_for_table()


def append_conclusions(indicators: list[list]) -> dict | None:
    """ Функция для добавления выводов о соответствии нормам в таблицу"""
    conclusions = ConclusionCreator(indicators)
    conclusions.append_conclusions()
    return conclusions.result_table


def add_conclusions_for_all_tables(tables_data):
    """ Добавить выводы о соответствии норм для всех таблиц. """
    for key, value in tables_data.items():
        if key[1] not in {'RESULTS', 'PROD_CONTROL'}:
            continue
        tables_data[key] = append_conclusions(value)
    return tables_data
