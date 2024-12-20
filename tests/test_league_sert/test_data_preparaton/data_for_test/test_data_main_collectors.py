""" Объекты класса MainCollector с уже собранными данными,
для проведения тестов."""

from league_sert.data_preparation.file_parser import MainCollector


def expected_collector_1():
    """Тестовый объект класса MainCollector"""
    main_collector = MainCollector('file')
    main_collector.main_number = '8281/24-Д'
    main_collector.main_date = '29 августа 2024'
    main_collector.prod_control_data = {
        'number_of_protocol': '8303/24-Д', 'date_of_protocol': '23 августа 2024',
        'act': '8303 ОТ 13.08.2024',
        'place_of_measurement': 'г. Калуга, ул. Ленина, д. 58, магазин № 40515',
        'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                            'уровни освещенности рабочей поверхности,'
                            ' шума и общей вибрации соответствуют требованиям'}
    main_collector.data_from_tables = {
        (1, 'MAIN'): {'Место отбора проб': 'г. Калуга, ул. Ленина, д.58 (№40515)',
                      'Юридический адрес': 'МО, г. Подольск, ул. Юбилейная, д. 32 А',
                      'Заявитель, ИНН': 'АО «ДИКСИ ЮГ», ИНН: 5036045205',
                      'Фактический адрес места осуществления деятельности':
                          'г. Калуга, ул. Ленина, д.58 (№40515)'},

        (2, 'store_prod'): {'Шифр пробы': '8281-1',
                            'Группа продукции': 'Производство магазина',
                            'Наименование продукции': 'Лепешка томаты с базиликом',
                            'Производитель (фирма, предприятие, организация)': 'АО «ДИКСИ ЮГ»',
                            'indicators': [{2: 2}, {9: 9}, {6: 6}]},

        (7, 'air'): {'indicators': [{1: 1}, ]},

        (9, 'washings'): {'indicators': [{9: 9}, ]},

        (12, 'PROD_CONTROL'): {'number_of_protocol': '8303/24-Д',
                               'date_of_protocol': '23 августа 2024',
                               'act': '8303 ОТ 13.08.2024',
                               'place_of_measurement': 'г. Калуга, ул. Ленина, д. 58, магазин № 40515',
                               'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                                                   'уровни освещенности рабочей поверхности, '
                                                   'шума и общей вибрации соответствуют требованиям',
                               'indicators': [{16: 16}]}
    }
    main_collector.keys_after_collect = [
        (1, 'MAIN'), (2, 'SAMPLE'), (4, 'RESULTS'), (5, 'RESULTS'), (6, 'RESULTS'),
        (7, 'SAMPLE'), (8, 'RESULTS'), (9, 'SAMPLE'), (10, 'RESULTS'), (12, 'PROD_CONTROL')]
    return main_collector


def expected_collector_2():
    """Тестовый объект класса MainCollector"""

    main_collector = MainCollector('file')
    main_collector.main_number = '7241/24-Д'
    main_collector.main_date = '25 июля 2024'
    main_collector.prod_control_data = {
        'number_of_protocol': '7248/24-Д',
        'date_of_protocol': '17 июля 2024',
        'act': '7248 ОТ 12.07.2024',
        'place_of_measurement': 'г. Москва, д. Яковлевское, д. 21. магазин № 50686',
        'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                            'уровни освещенности рабочей поверхности,'
                            ' шума и общей вибрации соответствуют требованиям'}

    main_collector.data_from_tables = {
        (0, 'MAIN'): {'Место отбора проб': 'г. Калуга, ул. Ленина, д.58 (№40515)',
                      'Юридический адрес': 'МО, г. Подольск, ул. Юбилейная, д. 32 А',
                      'Заявитель, ИНН': 'АО «ДИКСИ ЮГ», ИНН: 5036045205',
                      'Фактический адрес места осуществления деятельности':
                          'г. Калуга, ул. Ленина, д.58 (№40515)'},

        (1, 'store_prod'): {'Шифр пробы': '8281-1',
                            'Группа продукции': 'Производство магазина',
                            'Наименование продукции': 'Лепешка томаты с базиликом',
                            'Производитель (фирма, предприятие, организация)': 'АО «ДИКСИ ЮГ»',
                            'indicators': [{3: 3}]},
        (5, 'air'): {'indicators': [{1: 1}, ]},
        (7, 'washings'): {'indicators': [{9: 9}, ]},
        (10, 'PROD_CONTROL'): {
            'number_of_protocol': '7248/24-Д',
            'date_of_protocol': '17 июля 2024',
            'act': '7248 ОТ 12.07.2024',
            'place_of_measurement': 'г. Москва, д. Яковлевское, д. 21. магазин № 50686',
            'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                                'уровни освещенности рабочей поверхности, шума и общей '
                                'вибрации соответствуют требованиям',
            'indicators': [{1: 1}]}
    }
    main_collector.keys_after_collect = [
        (0, 'MAIN'), (1, 'SAMPLE'), (2, 'RESULTS'), (3, 'RESULTS'), (4, 'RESULTS'),
        (5, 'SAMPLE'), (6, 'RESULTS'), (7, 'SAMPLE'), (8, 'RESULTS'), (10, 'PROD_CONTROL')
    ]
    return main_collector


def expected_collector_3():
    """Тестовый объект класса MainCollector"""

    main_collector = MainCollector('file')
    main_collector.main_number = '6789/24-Д'
    main_collector.main_date = '22 июля 2024'
    main_collector.prod_control_data = {
        'number_of_protocol': '6792/24-Д',
        'date_of_protocol': '09 июля 2024',
        'act': '6792 от 05.07.2024',
        'place_of_measurement': 'г. Москва, ул. Юных Ленинцев, д. 43/33, магазин № 77189',
        'inner_conclusion': '- на момент проведения измерений параметры микроклимата, '
                            'уровни освещенности рабочей поверхности, '
                            'шума и общей вибрации соответствуют требованиям'}

    main_collector.data_from_tables = {
        (0, 'MAIN'): {'Место отбора проб': 'г. Калуга, ул. Ленина, д.58 (№40515)',
                      'Юридический адрес': 'МО, г. Подольск, ул. Юбилейная, д. 32 А',
                      'Заявитель, ИНН': 'АО «ДИКСИ ЮГ», ИНН: 5036045205',
                      'Фактический адрес места осуществления деятельности':
                          'г. Калуга, ул. Ленина, д.58 (№40515)'},

        (1, 'manuf_prod'): {'Шифр пробы': '8281-1',
                            'Группа продукции': 'Производство магазина',
                            'Наименование продукции': 'Лепешка томаты с базиликом',
                            'Производитель (фирма, предприятие, организация)': 'АО «ДИКСИ ЮГ»',
                            'indicators': [{3: 3}]},
        (4, 'manuf_prod'): {'indicators': [{1: 1}, ]},
        (6, 'manuf_prod'): {'indicators': [{9: 9}, ]},
        (10, 'manuf_prod'): {'indicators': [{9: 9}, ]},
        (12, 'air'): {'indicators': [{9: 9}, ]},
        (15, 'PROD_CONTROL'): {'indicators': [{9: 9}, ]},
    }

    main_collector.keys_after_collect = [
        (0, 'MAIN'), (1, 'SAMPLE'), (2, 'RESULTS'), (4, 'SAMPLE'),
        (5, 'RESULTS'), (6, 'SAMPLE'), (7, 'RESULTS'), (9, 'RESULTS'),
        (10, 'SAMPLE'), (11, 'RESULTS'), (12, 'SAMPLE'), (13, 'RESULTS'),
        (15, 'PROD_CONTROL')
    ]

    return main_collector
