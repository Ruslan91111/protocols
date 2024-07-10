import re
import time
from enum import Enum


FOR_REPLACE_IN_DEGREE = {
    '⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4,
    '⁵': 5, '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9
}


class ComparisonTypes(Enum):
    """ Тип сравнения в зависимости от содержания в поле норма. """
    within: str = r'\d+\,?\d*\s?-\s?\d+\,?\d*\b'  # 2,0 - 4,2
    up_to: str = r'\bдо\b\s\d+\,?\d*\b'  # до 1,5
    not_allowed: str = r'\bне допускаются в \d+\,?\d*\s?[а-я]?'  # не допускаются в 0,1 г
    at_least: str = r'\bне менее \d+\,?\d*\s?'  # не менее 9,0
    no_more: str = r'\bне более \d+\,?\d*'  # не более 220,0


class ConversionTypesOfValue(Enum):
    """ Тип сравнения в зависимости от содержания в поле норма. """
    plus: str = r'\d\s?[+±]\s?\d'  # 16,34±0,15;  +
    multiplication: str = r'\d\s?[•■]\s?\d'  # 1 ■ 101², 1 • 10²
    no_more: str = r'до \d+,?\d*'  # до 1,5
    within: str = r'\d+\,?\d*\s?-\s?\d+\,?\d*\b'  # 2,0 - 4,2
    less: str = r'менее \d+,?\d*'  # менее 0,10
    not_found: str = r'не обнаружено'  # не обнаружено в 25,0 г
    digit: str = r'\d+,?\d*'  # 9,0


def find_out_type_of_the_value(
        value: str, types_of_value: [ComparisonTypes | ConversionTypesOfValue]
) -> str:
    """ Принимает значение и класс enum, перебирает паттерны из класса enum,
    находит тип, подходящий под значение и возвращает его. """
    for type_value in types_of_value:
        if re.search(type_value.value, value.lower()):
            return type_value.name
    return ''


def convert_numbers_with_degrees(value: str) -> str:
    pattern_for_numbers_with_degrees = r'(\d+\.?\d*\s?[•■-]\s?)(\d*[⁰¹²³⁴⁵⁶⁷⁸⁹])'
    match = re.search(pattern_for_numbers_with_degrees, value)
    if match:
        numbers_with_degrees = match.group(2)
        result = 10 ** int(numbers_with_degrees[2])
        replacement = r'\g<1>%s' % (result)
        updated_value = re.sub(pattern_for_numbers_with_degrees, replacement, value)
        return updated_value
    return value


def process_the_value(value: str, type_of_processing: str) -> int | float | list:
    """
    Получить на вход значение в виде строки, преобразовать строку
    в значение для выполнения сравнения.
    """

    if type_of_processing == ConversionTypesOfValue.plus.name:
        pattern = r'(\d+[,\.]?\d*)'
        match = re.findall(pattern, value)
        return sum([float(i.replace(',', '.')) for i in match])

    elif type_of_processing == ConversionTypesOfValue.multiplication.name:
        pattern = r'(\d+[,\.]?\d*)\s?([•■]+\s?)(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)'
        match_substring = re.search(pattern, value)
        first_digit = match_substring.group(1).replace(',', '.')
        second_digit = match_substring.group(3).replace(',', '.')
        degree = match_substring.group(4)
        degree = FOR_REPLACE_IN_DEGREE[degree]
        result = float(first_digit) * (float(second_digit) ** degree)
        return result

    elif type_of_processing == ConversionTypesOfValue.not_found.name:
        return 0

    elif type_of_processing == ConversionTypesOfValue.within.name:
        pattern = r'(\d+[,\.]?\d*)'
        match = re.findall(pattern, value)
        if match:
            return [float(i.replace(',', '.')) for i in match]
    else:
        pattern = r'(\d+[,\.]?\d*)'
        match = re.search(pattern, value)
        if match:
            return float(match.group(0).replace(',', '.'))
        return 0


def compare_result_and_norms(result: str, norm: str) -> bool:
    """ Сравнить результат исследования с нормой и
    вернуть соответствует ли результат нормам или нет."""

    type_of_processing_for_value_of_result = find_out_type_of_the_value(result, ConversionTypesOfValue)
    type_of_processing_for_value_of_norm = find_out_type_of_the_value(norm, ConversionTypesOfValue)
    value_of_result = process_the_value(result, type_of_processing_for_value_of_result)
    value_of_norm = process_the_value(norm, type_of_processing_for_value_of_norm)
    type_of_comparison = find_out_type_of_the_value(norm, ComparisonTypes)

    if type_of_comparison == ComparisonTypes.within.name:
        if value_of_norm[0] < value_of_result <= value_of_norm[1]:
            return True
        return False

    if type_of_comparison == "up_to":
        if value_of_norm > value_of_result:
            return True
        return False

    if type_of_comparison == "not_allowed":
        if value_of_result == 0:
            return True
        return False

    if type_of_comparison == "at_least":
        if value_of_result > value_of_norm:
            return True
        return False

    if type_of_comparison == "no_more":
        if value_of_result < value_of_norm:
            return True
        else:
            return False

