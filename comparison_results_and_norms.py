""" Модуль с функцией для сравнения и вывода соответствуют ли результаты исследований нормам.

    def compare_result_and_norms - принимает на вход два параметра:
      :param - value: str - показатель результат исследования.
      :norm - value: str - показатель необходимые требования к данному показателю.

      :return bool: True - если нарушений не обнаружено
      :return bool: False - если имеется нарушение норм

      Пример использования compare_result_and_norms(result, norm)
"""
import re


TYPES_OF_STATUSES_OF_NORMS = ('отсутствие',
                              'не более',
                              'не допускаются',
                              '-')

TYPES_OF_STATUSES_OF_RESULTS = (r'не обнаружен[о ы]',
                                'не более',
                                '<',
                                '-',
                                '±',
                                '0')

PATTERNS_FOR_SEARCH_VALUE = r'\d+[\.|,]?\d*'


def _find_out_type_of_the_value(value: str, statuses: tuple) -> str:
    """ Определить тип значения, переданного в функцию.
     В функцию передается значение из колонки 'Результат' или 'Требования НД'
     и соответствующее множество с типами значений.
     Возвращается тип значения из множества. """
    for status in statuses:
        if re.search(status, value.lower()):
            return status
    return ''


def compare_result_and_norms(result: str, norm: str) -> bool:
    """ Сравнить результат исследования с нормой и
    вернуть соответствует ли результат нормам или нет."""

    type_of_result = _find_out_type_of_the_value(result, TYPES_OF_STATUSES_OF_RESULTS)
    type_of_norm = _find_out_type_of_the_value(norm, TYPES_OF_STATUSES_OF_NORMS)

    if (type_of_norm in {'отсутствие', 'не допускаются', '-'} and
            type_of_result in {'не обнаружен[о ы]', '0', '-'}):
        return True

    if (type_of_norm in {'отсутствие', 'не допускаются', '-'} and
            type_of_result in {'<', 'не более'}):
        result_value_digit = float(re.search(PATTERNS_FOR_SEARCH_VALUE, result).
                                   group().replace(',', '.'))
        if result_value_digit and result_value_digit < 0.1:
            return True
        return False

    if type_of_norm == 'не более':
        if '±' in result:
            plus_minus_index = result.find('±')
            result_base_value = float(result[:plus_minus_index].replace(",", '.'))
            tolerance = float(result[plus_minus_index + 1:].replace(',', '.'))
            result_value_with_tolerance = result_base_value + tolerance
            norm_value = float(re.search(PATTERNS_FOR_SEARCH_VALUE, norm).group().replace(',', '.'))
            if result_value_with_tolerance < norm_value:
                return True

        result_value_digit = float(re.search(PATTERNS_FOR_SEARCH_VALUE,
                                             result).group().replace(',', '.'))

        if result_value_digit == 0:
            return True

        norm_value_digit = float(re.search(PATTERNS_FOR_SEARCH_VALUE, norm).
                                 group().replace(',', '.'))
        if result_value_digit and norm_value_digit and (result_value_digit <= norm_value_digit):
            return True

    return False
