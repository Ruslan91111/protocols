""" Тестирование модуля launch_data_preparation"""

from league_sert.data_preparation.launch_data_preparation import extract_and_prepare_data
from tests.test_league_sert.test_data_preparation.expected_data_from_launch import \
    EXPECTED_FROM_PARSER


def test_extract_and_prepare_data():
    """ Тестирование основной функции модуля. Проверка, что результат всей работы по
    извлечению, преобразованию, добавлению выводов соответствует ожидаемому. """
    data_result = extract_and_prepare_data(r'47109 23.05.2024.docx')
    print('!!!!!!!!!', data_result.data_from_tables.keys())
    assert list(data_result.data_from_tables.keys()) == [
        (0, 'MAIN'),
        (1, 'manuf_prod'),
        (3, 'manuf_prod'),
        (5, 'manuf_prod'),
        (8, 'manuf_prod'),
        (10, 'air'),
        (13, 'PROD_CONTROL')
    ]
    assert data_result.main_number == '4225/24-Д'
    assert data_result.main_date == '23 мая 2024'
