""" Модуль для сравнения результатов исследований и норм.

Классы:
    - ValueProcessor:
        Класс обработки значений, принимает при инициализации значение и тип значения.
        Новое, значение, подготовленное для сравнения присваивает атрибуту - self.new_value.

    - ComparatorResNorms:
        Класс для сравнения результатов исследования с нормами.
        Вывод о соответствии нормам присваивается атрибуту - self.conclusion.
        В своей работе создает и использует объекты класса ValueProcessor

Функции:
    - define_value_type:
        Принимает значение и класс enum, перебирает паттерны из класса enum,
        находит тип, подходящий под значение и возвращает его.

    - to_process_the_value:
        Обработать значение и вернуть в преобразованном виде.
        Функция для использования класса ValueProcessor

    - create_conformity_conclusion:
        Функция для сравнения результатов исследования с нормой.
        Возвращает либо bool если значение результат исследования одно число,
        и list[bool] если значение результата исследования имеет погрешность
        в виде '±'. В своей работе создает и оперирует классом CompareResultAndNorms.


enum классы:
    - ComparisonTypes:
        Тип сравнения в зависимости от содержания в поле норма,
        для определения логики, используемой при сравнении.

    - ConversionTypes:
        Тип сравнения в зависимости от содержания в поле норма.

Пример использования:
    - conclusion = compare_result_and_norms(result: str, norm: str)

"""
import re
from enum import Enum

FOR_REPLACE_IN_DEGREE = {'⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4,
                         '⁵': 5, '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9}


class ComparisonTypes(Enum):
    """ Тип сравнения в зависимости от содержания в поле норма,
    для определения логики, используемой при сравнении. """
    within: str = r'\d+\,?\d*\s?-\s?\d+\,?\d*\b'  # 2,0 - 4,2
    up_to: str = r'\bдо\b\s\d+\,?\d*\b'  # до 1,5
    not_allowed: str = r'\bне допускаются в \d+\,?\d*\s?[а-я]?|^\-$'  # не допускаются в 0,1 г
    at_least: str = r'\bне менее \d+\,?\d*\s?'  # не менее 9,0
    no_more: str = r'\bне более \d+\,?\d*'  # не более 220,0


class ConversionTypes(Enum):
    """ Тип сравнения в зависимости от содержания в поле норма. """
    plus: str = r'\d\s?[+±]\s?\d'  # 16,34±0,15;  +
    multiplication: str = r'\d\s?[•■]\s?\d'  # 1 ■ 101², 1 • 10²
    no_more: str = r'до \d+,?\d*'  # до 1,5
    within: str = r'\d+\,?\d*\s?-\s?\d+\,?\d*\b'  # 2,0 - 4,2
    less: str = r'менее \d+,?\d*'  # менее 0,10
    not_found: str = r'не обнаружено'  # не обнаружено в 25,0 г
    digit: str = r'\d+,?\d*'  # 9,0
    none: str = r'^\-$'  # '-'


def create_conformity_conclusion(result: str, norm: str) -> bool | list[bool]:
    """ Функция для сравнения результатов исследования с нормой.
     Возвращает либо bool если значение результат исследования одно число,
     и list[bool] если значение результата исследования имеет погрешность
     в виде '±' """
    comparer = ComparatorResNorms(result, norm)
    comparer.compare()
    return comparer.conclusion


def define_value_type(value: str, types_of_value: [ComparisonTypes | ConversionTypes]) -> str:
    """ Принимает значение и класс enum, перебирает паттерны из класса enum,
    находит тип, подходящий под значение и возвращает его. """
    for type_value in types_of_value:
        if re.search(type_value.value, value.lower()):
            return type_value.name
    return ''


class ValueProcessor:
    """ Класс обработчик значений.
    Задача обработать значение и преобразовать в подходящий для сравнения вид. """
    def __init__(self, value: str, type_of_processing: str):
        """ Конструктор - принимает само значение и тип значения. """
        self.value = value  # Само значение
        self.type_of_processing = type_of_processing  # Тип значения
        self.types = ConversionTypes
        self.process_the_value()  # Значение в результате обработки

    def process_for_plus(self):
        """ Обработать значение для показателей плюс-минус.
        Результат - два числа: основное и с отклонением. """
        pattern = r'(\d+[,\.]?\s?\d*)'
        match = re.findall(pattern, self.value)
        main_digit = float(match[0].replace(',', '.').replace(' ', ''))
        deviation = float(match[1].replace(',', '.').replace(' ', ''))
        self.new_value: list = [main_digit, main_digit + deviation]

    def process_multiplication(self):
        """ Обработать значение для показателей с двумя перемножающимися числами,
        в том числе, со степенью. Вычисляет значение с учетом степени.  """
        pattern = r'(\d+[,\.]?\d*)\s?([•■]+\s?)(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)'
        match_substr = re.search(pattern, self.value)
        first_digit = match_substr.group(1).replace(',', '.')
        second_digit = match_substr.group(3).replace(',', '.')
        degree = match_substr.group(4)
        degree = FOR_REPLACE_IN_DEGREE[degree]
        self.new_value = float(first_digit) * (float(second_digit) ** degree)

    def process_within(self):
        """ Обработать значение для показателей с пределами: "2,0 - 4,2".
        Заменить ',' на '.' """
        pattern = r'(\d+[,\.]?\d*)'
        match = re.findall(pattern, self.value)
        if match:
            self.new_value = [float(i.replace(',', '.')) for i in match]

    def process_other(self):
        """ Обработать не указанные ранее варианты,
        в основном для значений в виде числа.  """
        pattern = r'(\d+[,\.]?\d*)'
        match = re.search(pattern, self.value)
        if match:
            self.new_value = float(match.group(0).replace(',', '.'))
        else:
            self.new_value = 0

    def process_the_value(self):
        """ Преобразовать строку в значение для выполнения сравнения.
        Выбор логики преобразования в зависимости от типа значения.
        Результат преобразования будет сохранен в атрибут self.new_value"""
        if self.type_of_processing == self.types.plus.name:
            self.process_for_plus()
        elif self.type_of_processing == self.types.multiplication.name:
            self.process_multiplication()
        elif (self.type_of_processing == self.types.not_found.name or
              self.type_of_processing == self.types.none.name):
            self.new_value = 0
        elif self.type_of_processing == self.types.within.name:
            self.process_within()
        else:
            self.process_other()


def to_process_the_value(value: str):
    """ Обработать значение и вернуть в преобразованном виде.
    Функция для использования класса ValueProcessor"""
    value_type = define_value_type(value, ConversionTypes)
    return ValueProcessor(value, value_type).new_value


class ComparatorResNorms:
    """  Класс для сравнения результатов исследования с нормами.
    если показатель соответствует норме, то self.conclusion = True. """
    def __init__(self, result: str, norm: str):
        self.comparison_type = define_value_type(norm, ComparisonTypes)
        self.result = to_process_the_value(result)  # Результат исследования
        self.norm = to_process_the_value(norm)  # Нормы
        self.conclusion = None  # Вывод о наличии нарушений нормам.

    def compare_within(self):
        """ Сравнение, когда нормы определены в виде нижнего
         и верхнего допустимого значения. """
        if isinstance(self.result, list):
            self.conclusion = (self.norm[0] < self.result[0] <= self.norm[1],
                               self.norm[0] < self.result[1] <= self.norm[1])
        else:
            self.conclusion = self.norm[0] < self.result <= self.norm[1]

    def compare_up_to(self):
        """ Сравнение, когда нормы определены в виде
        'до определенного значения'. """
        if isinstance(self.result, list):
            self.conclusion = (self.result[0] <= self.norm, self.result[1] <= self.norm)
        else:
            self.conclusion = self.result <= self.norm

    def compare_not_allowed(self):
        """ Сравнение, когда нормы определены в виде
        'не допускаются'. """
        self.conclusion = (self.result == 0)

    def compare_at_least(self):
        """ Сравнение, когда нормы определены в виде
        'не менее определенного значения'. """
        if isinstance(self.result, list):
            self.conclusion = (self.result[0] > self.norm, self.result[1] > self.norm)
        else:
            self.conclusion = self.result >= self.norm

    def compare_no_more(self):
        """ Сравнение, когда нормы определены в виде
        'не более определенного значения'. """
        if isinstance(self.result, list):
            self.conclusion = (self.result[0] <= self.norm, self.result[1] <= self.norm)
        else:
            self.conclusion = self.result <= self.norm

    def compare(self):
        """ Выполнение операции сравнения в зависимости от типа сравнения. """
        if self.comparison_type == ComparisonTypes.within.name:
            self.compare_within()

        elif self.comparison_type == ComparisonTypes.up_to.name:
            self.compare_up_to()

        elif self.comparison_type == ComparisonTypes.not_allowed.name:
            self.compare_not_allowed()

        elif self.comparison_type == ComparisonTypes.at_least.name:
            self.compare_at_least()

        elif self.comparison_type == ComparisonTypes.no_more.name:
            self.compare_no_more()
