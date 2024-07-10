"""
Тестируем код из модуля fbu_comparison_results_and_norms.py

    Тестируем определение типа сравнения.
    Тестируем определение типа для преобразования данных из протокола.
    Тестируем определение типа для преобразования данных из протокола.

"""

import pytest

from fbu_comparison_results_and_norms import (find_out_type_of_the_value,
                                              ComparisonTypes,
                                              ConversionTypesOfValue,
                                              process_the_value,
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
    received_result = find_out_type_of_the_value(value, types_of_value)
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
    received_result = find_out_type_of_the_value(value, types_of_value)
    assert received_result == expected_type_of_value


@pytest.mark.parametrize("value, type_of_processing, expected_result",
                         [
                             ("16,34±0,15;", ConversionTypesOfValue.plus.name, 16.49),
                             ("16,34+0,15;", ConversionTypesOfValue.plus.name, 16.49),
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
