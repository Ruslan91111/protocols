import datetime

import pytest

from league_sert.models.models_creator import split_code_and_address, create_date


@pytest.mark.parametrize('text, expected_address, expected_code',
                         [
                             ('г. Кострома, ул. Юрия Беленогова, д. 17 А (44433)',
                              'г. Кострома, ул. Юрия Беленогова, д. 17 А',
                              44433),
                             ('Ленинградская область, Гатчинский р-н, '
                              'г. Гатчина, ул. Куприна, д. 48, л. А (№47109)',
                              'Ленинградская область, Гатчинский р-н, г. Гатчина, ул. Куприна, д. 48, л. А',
                              47109),
                             ('№ 47190, Ленинградская обл., Гатчинский р-н, п. Вырица, ул. Футбольная, Д. 29',
                              'Ленинградская обл., Гатчинский р-н, п. Вырица, ул. Футбольная, Д. 29',
                              47190),
                             ('МО, Сергиево-Посадский район, г. Сергиев Посад, ул. Куликова, д. 21А (№ 50445)',
                              'МО, Сергиево-Посадский район, г. Сергиев Посад, ул. Куликова, д. 21А',
                              50445),
                             ('г. Москва, ул. 1-я Рейсовая, д.12, корп.1 (№77367)',
                              'г. Москва, ул. 1-я Рейсовая, д.12, корп.1',
                              77367),
                             ('(№77367) г. Москва, ул. 1-я Рейсовая, д.12, корп.1',
                              'г. Москва, ул. 1-я Рейсовая, д.12, корп.1',
                              77367),
                         ])
def test_split_code_and_address(text, expected_address, expected_code):
    address, code = split_code_and_address(text)
    assert isinstance(address, str)
    assert isinstance(code, int)
    assert address == expected_address
    assert code == expected_code


@pytest.mark.parametrize('date_, expected_date',
                         [
                             ('11 мая 2024', datetime.date(2024, 5, 11)),
                             ('11 мая 2024 г.', datetime.date(2024, 5, 11)),
                             ('11 мая 2024 года', datetime.date(2024, 5, 11)),
                             ('11  мая   2024 г.', datetime.date(2024, 5, 11))
                         ])
def test_create_date(date_, expected_date):
    received_date = create_date(date_)
    assert isinstance(received_date, datetime.date)
    assert received_date == expected_date
