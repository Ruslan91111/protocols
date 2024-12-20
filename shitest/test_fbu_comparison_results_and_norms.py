"""
Тестируем код из модуля fbu_comparison_results_and_norms.py

    Тестируем определение типа сравнения.
    Тестируем определение типа для преобразования данных из протокола.
    Тестируем определение типа для преобразования данных из протокола.
    Тестируем определение вывода по соответствию результат исследования нормам.

"""

import pytest

from fbu_comparison_results_and_norms import (define_value_type,
                                              ComparisonTypes,
                                              ConversionTypesOfValue,
                                              process_the_value, compare_result_and_norms,
                                              )


@pytest.mark.parametrize("value, expected_type_of_comparison",
                         [
                             ("2,0 - 4,2", "within"),
                             ("до 1,5", "up_to"),
                             ("не допускаются в 0,1 г", "not_allowed"),
                             ("не менее 9,0", "at_least"),
                             ("не более 220,0", "no_more"),
                             ("набор букв", ""),
                             ("не менее 1 ■ 106", 'at_least'),
                         ])
def test_find_out_type_of_comparison(value,
                                     expected_type_of_comparison,
                                     types_of_value=ComparisonTypes):
    """
    Тестируем определение типа сравнения.
    """
    received_result = define_value_type(value, types_of_value)
    assert received_result == expected_type_of_comparison


@pytest.mark.parametrize("value, expected_type_of_value",
                         [
                             ("16,34±0,15;", ConversionTypesOfValue.plus.name),
                             ("16,34+0,15;", ConversionTypesOfValue.plus.name),
                             ("1 • 101", ConversionTypesOfValue.multiplication.name),
                             ("менее 1 ■ 10¹", ConversionTypesOfValue.multiplication.name),
                             ("2,5 • 10⁶", ConversionTypesOfValue.multiplication.name),
                             ("до 1,5", ConversionTypesOfValue.no_more.name),
                             ("2,0 - 4,2", ConversionTypesOfValue.within.name),
                             ("менее 0,10", ConversionTypesOfValue.less.name),
                             ("не обнаружено в 25,0 г", ConversionTypesOfValue.not_found.name),
                             ("набор букв", ""),
                             ("9,0", ConversionTypesOfValue.digit.name),
                         ])
def test_find_out_type_of_the_value(value,
                                    expected_type_of_value,
                                    types_of_value=ConversionTypesOfValue):
    """
    Тестируем определение типа для преобразования данных из протокола.
    """
    received_result = define_value_type(value, types_of_value)
    assert received_result == expected_type_of_value


@pytest.mark.parametrize("value, type_of_processing, expected_result",
                         [
                             ("16,34±0,15;", ConversionTypesOfValue.plus.name, [16.34, 16.49]),
                             ("16,34+0,15;", ConversionTypesOfValue.plus.name, [16.34, 16.49]),
                             ("1 • 10¹", ConversionTypesOfValue.multiplication.name, 10),
                             ("менее 1 ■ 10¹", ConversionTypesOfValue.multiplication.name, 10),
                             ("2,5 • 10⁶", ConversionTypesOfValue.multiplication.name, 2500000),
                             ("до 1,5", ConversionTypesOfValue.no_more.name, 1.5),
                             ("2,0 - 4,2", ConversionTypesOfValue.within.name, [2.0, 4.2]),
                             ("менее 0,10", ConversionTypesOfValue.less.name, 0.10),
                             ("не обнаружено в 25,0 г", ConversionTypesOfValue.not_found.name, 0),
                             ("набор букв", "", 0),
                             ("9,0", ConversionTypesOfValue.digit.name, 9.0),
                         ])
def test_process_the_value(value,
                           type_of_processing,
                           expected_result):
    """
    Тестируем определение типа для преобразования данных из протокола.
    """
    received_result = process_the_value(value, type_of_processing)
    assert received_result == expected_result


@pytest.mark.parametrize("result, norm, expected_result",
                         [
                             ('3,02+0,4', '2,0 - 4,2', (True, True)),
                             ('1,90+0,4', '1,5 - 3,0', (True, True)),
                             ('3,16+0,4', '2,0 - 3,5', (True, False)),
                             ('0,31+0,4', '0,2 - 0,4', (True, False)),
                             ('3,68+0,4', '2,0 - 4,0', (True, False)),
                             ('11,80+2,2', '8,0 - 13,0', (True, False)),
                             ('9, 0', 'не менее 9, 0', True),
                             ('менее 1 ■ 10¹', 'не более 100', True),
                             ('10, 05+2,2', '9,0 - 14,0', (True, True)),
                             ('23, 62+2,2', '22,0 - 33,0', (True, True)),
                             ('не обнаружено в 0,01 г', 'не допускаются в 0,01 г', True),
                             ('2,5-10⁶', 'не менее 1-10⁶', True),
                             ('менее 1 • 10¹', 'не более 50', True)
                         ])
def test_compare_result_and_norms(result, norm, expected_result):
    """ Тестируем определение вывода по соответствию результат исследования нормам
    для каждого показателя. """
    received_result = compare_result_and_norms(result, norm)
    assert received_result == expected_result
