""" Место хранения фикстур, которые будут использоваться несколькими файлами тестов"""
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main_file import ProtocolToDBWorker
from models import Base
from work_with_tables_in_db import StoreManager, ProtocolManager


@pytest.fixture(autouse=True)
def change_test_dir(request):
    os.chdir(request.fspath.dirname)


@pytest.fixture(scope='module')
def test_engine():
    """ Создать тестовый движок базы данных. """
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope='function')
def test_session(test_engine):
    """ Создать тестовую сессию с БД. """
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    Session = sessionmaker(bind=test_engine, expire_on_commit=False)
    session = Session
    yield session
    # session.close()


@pytest.fixture
def store_manager(test_session):
    """ Создать экземпляр StoreManager с тестовой сессией. """
    manager = StoreManager(test_session)
    return manager


@pytest.fixture
def protocol_manager(test_session):
    """ Создать экземпляр ProtocolManager с тестовой сессией. """
    manager = ProtocolManager(test_session)
    return manager


@pytest.fixture
def protocol_to_db_worker(test_session):
    """ Создать экземпляр StoreManager с тестовой сессией. """
    manager = ProtocolToDBWorker(test_session)
    return manager


@pytest.fixture
def data_from_word_file_1():
    return {'Номер протокола': '№13435/23-Д', 'Дата протокола': '27 декабря 2023', 'Место отбора проб': '77030',
            'Дата и время отбора проб': '18.12.2023 г., И ч. 00 мин.',
            'Сопроводительные документы': 'Акт отбора проб № 13435 от 18.12.2023 г.',
            'Группа продукции': 'Продукция производителя',
            'Наименование продукции': 'Молоко питьевое пастеризованное м. д. жира 3,2%',
            'Дата производства продукции': '14.12.2023 г. Годен до 30.12.2023 г.',
            'Производитель (фирма, предприятие, организация)': 'ООО «Милк Экспресс»',
            'Дата проведения исследований': '18.12.2023 г.-24.12.2023 г.', 'Показатели': [
            {'Массовая доля сорбиновой кислоты, мг/кг': ('<20', 'не более 2000', True),
             'Массовая доля бензойной кислоты, мг/кг': ('<20', '-', False)},
            {'Токсичные элементы, мг/кг:': ('Токсичные элементы, мг/кг:', 'Токсичные элементы, мг/кг:', '-'),
             '- свинец': ('0,185±0,055', 'не более 0,35', True), '- мышьяк': ('<0,05', 'не более 0,15', True),
             '- кадмий': ('0,005±0,002', 'не более 0,07', True), '- ртуть': ('< 0,002', 'не более 0,015', True),
             'Пестициды, мг/кг:': ('Пестициды, мг/кг:', 'Пестициды, мг/кг:', '-'),
             '- ГХЦГ(а, р, у - изомеры)': ('<0,01', 'не более 0,5', True),
             '- ДДТ и его метаболиты': ('<0,01', 'не более 0,02', True),
             '-гексахлорбензол': ('<0,01', 'не более 0,01', True),
             '- ртутьорганические': ('<0,01', 'не допускаются', True),
             '- 2,4-Д кислота, ее соли, эфиры': ('<0,02', 'не допускаются', True)}, {
                'Количество мезофильных, аэробных и факультативно-анаэробных микроорганизмов, КОЕ/см3': (
                    '3,0х103', 'не более 1,0x10s', False),
                'БГКП (колиформы)': ('не обнаружены в 0,01 см3', 'не допускаются в 0,01 см3', True),
                'S. aureus': ('не обнаружено в 1,0 см3', 'не допускаются в 1,0 см3', True),
                'L. monocytogenes': ('не обнаружено в 25 см3', 'не допускаются в 25 см3', True),
                'Патогенные микроорганизмы, в т.ч. сальмонеллы': (
                    'не обнаружено в 25 см3', 'не допускаются в 25 см3', True)}], 'Нарушения норм': 'Не соответствуют'}


@pytest.fixture
def data_from_word_file_2():
    return {'Номер протокола': '№13432/23-Д', 'Дата протокола': '27 декабря 2023', 'Место отбора проб': '90344',
            'Дата и время отбора проб': '18.12.2023 г., 14 ч. 10 мин.',
            'Сопроводительные документы': 'Акт отбора проб № 13432 от 18.12.2023 г.',
            'Группа продукции': 'Производство магазина',
            'Наименование продукции': 'Улитка греческая «Косичка» с курицей, рисом и овощами',
            'Дата производства продукции': '27.09.2023 г. Годен до 27.09.2024 г.',
            'Производитель (фирма, предприятие, организация)': 'АО «Дикси ЮГ» №90344',
            'Дата проведения исследований': '18.12.2023 г.-24.12.2023 г.', 'Показатели': [
            {'Массовая доля сорбиновой кислоты, мг/кг': ('90,2±10,0', 'не более 2000', True),
             'Массовая доля бензойной кислоты, мг/кг': ('<20', '-', False)},
            {'Токсичные элементы, мг/кг:': ('Токсичные элементы, мг/кг:', 'Токсичные элементы, мг/кг:', '-'),
             '- свинец': ('0,140±0,042', 'не более 0,35', True), '- мышьяк': ('<0,05', 'не более 0,15', True),
             '- кадмий': ('0,003±0,001', 'не более 0,07', True), '- ртуть': ('< 0,002', 'не более 0,015', True),
             'Пестициды, мг/кг:': ('Пестициды, мг/кг:', 'Пестициды, мг/кг:', '-'),
             '- ГХЦГ(а, р, у - изомеры)': ('<0,01', 'не более 0,5', True),
             '- ДДТ и его метаболиты': ('<0,01', 'не более 0,02', True),
             '-гексахлорбензол': ('<0,01', 'не более 0,01', True),
             '- ртутьорганические': ('<0,01', 'не допускаются', True),
             '- 2,4-Д кислота, ее соли, эфиры': ('<0,02', 'не допускаются', True)}],
            'Нарушения норм': 'Не соответствуют'}


@pytest.fixture
def data_from_word_file_3():
    return {'Номер протокола': '№13509/23-Д', 'Дата протокола': '29 декабря 2023', 'Место отбора проб': '77029',
            'Дата и время отбора проб': '19.12.2023 г., 08 ч. 55 мин.',
            'Сопроводительные документы': 'Акт отбора проб № 13509 от 19.12.2023 г.',
            'Группа продукции': 'Производство магазина',
            'Наименование продукции': 'Улитка греческая косичка с сыром и картофелем',
            'Дата производства продукции': '19.12.2023 г. Срок годности 24 часа',
            'Производитель (фирма, предприятие, организация)': 'АО «Дикси ЮГ»',
            'Дата проведения исследований': '19.12.2023 г.-25.12.2023 г.', 'Показатели': [
            {'Массовая доля сорбиновой кислоты, мг/кг': ('<20', 'не более 2000', True),
             'Массовая доля бензойной кислоты, мг/кг': ('<20', '-', False)},
            {'Токсичные элементы, мг/кг:': ('Токсичные элементы, мг/кг:', 'Токсичные элементы, мг/кг:', '-'),
             '- свинец': ('0,048±0,019', 'не более 0,35', True), '- мышьяк': ('<0,05', 'не более 0,15', True),
             '- кадмий': ('0,011±0,004', 'не более 0,07', True), '- ртуть': ('< 0,002', 'не более 0,015', True),
             'Пестициды, мг/кг:': ('Пестициды, мг/кг:', 'Пестициды, мг/кг:', '-'),
             '- ГХЦГ(а, Р, у - изомеры)': ('<0,01', 'не более 0,5', True),
             '- ДДТ и его метаболиты': ('<0,01', 'не более 0,02', True),
             '- гексахлорбензол': ('<0,01', 'не более 0,01', True),
             '- ртутьорганические': ('<0,01', 'не допускаются', True),
             '- 2,4-Д кислота, ее соли, эфиры': ('<0,02', 'не допускаются', True)}],
            'Нарушения норм': 'Не соответствуют'}


@pytest.fixture
def data_from_db_1():
    return {'Номер протокола': '№13435/23-Д', 'Дата протокола': '27 декабря 2023',
            'Место отбора проб': 77030,
            'Дата и время отбора проб': '18.12.2023 г., И ч. 00 мин.',
            'Сопроводительные документы': 'Акт отбора проб № 13435 от 18.12.2023 г.',
            'Группа продукции': 'Продукция производителя',
            'Наименование продукции': 'Молоко питьевое пастеризованное м. д. жира 3,2%',
            'Дата производства продукции': '14.12.2023 г. Годен до 30.12.2023 г.',
            'Производитель (фирма, предприятие, организация)': 'ООО «Милк Экспресс»',
            'Дата проведения исследований': '18.12.2023 г.-24.12.2023 г.', 'Показатели': [
            {'Массовая доля сорбиновой кислоты, мг/кг': ['<20', 'не более 2000', True],
             'Массовая доля бензойной кислоты, мг/кг': ['<20', '-', False]},
            {'Токсичные элементы, мг/кг:': ['Токсичные элементы, мг/кг:', 'Токсичные элементы, мг/кг:', '-'],
             '- свинец': ['0,185±0,055', 'не более 0,35', True], '- мышьяк': ['<0,05', 'не более 0,15', True],
             '- кадмий': ['0,005±0,002', 'не более 0,07', True], '- ртуть': ['< 0,002', 'не более 0,015', True],
             'Пестициды, мг/кг:': ['Пестициды, мг/кг:', 'Пестициды, мг/кг:', '-'],
             '- ГХЦГ(а, р, у - изомеры)': ['<0,01', 'не более 0,5', True],
             '- ДДТ и его метаболиты': ['<0,01', 'не более 0,02', True],
             '-гексахлорбензол': ['<0,01', 'не более 0,01', True],
             '- ртутьорганические': ['<0,01', 'не допускаются', True],
             '- 2,4-Д кислота, ее соли, эфиры': ['<0,02', 'не допускаются', True]}, {
                'Количество мезофильных, аэробных и факультативно-анаэробных микроорганизмов, КОЕ/см3': ['3,0х103',
                                                                                                         'не более 1,0x10s',
                                                                                                         False],
                'БГКП (колиформы)': ['не обнаружены в 0,01 см3', 'не допускаются в 0,01 см3', True],
                'S. aureus': ['не обнаружено в 1,0 см3', 'не допускаются в 1,0 см3', True],
                'L. monocytogenes': ['не обнаружено в 25 см3', 'не допускаются в 25 см3', True],
                'Патогенные микроорганизмы, в т.ч. сальмонеллы': ['не обнаружено в 25 см3', 'не допускаются в 25 см3',
                                                                  True]}],
            'Нарушения норм': 'Не соответствуют'}


@pytest.fixture
def data_from_db_2():
    return {'Номер протокола': '№13432/23-Д', 'Дата протокола': '27 декабря 2023',
            'Место отбора проб': 90344,
            'Дата и время отбора проб': '18.12.2023 г., 14 ч. 10 мин.',
            'Сопроводительные документы': 'Акт отбора проб № 13432 от 18.12.2023 г.',
            'Группа продукции': 'Производство магазина',
            'Наименование продукции': 'Улитка греческая «Косичка» с курицей, рисом и овощами',
            'Дата производства продукции': '27.09.2023 г. Годен до 27.09.2024 г.',
            'Производитель (фирма, предприятие, организация)': 'АО «Дикси ЮГ» №90344',
            'Дата проведения исследований': '18.12.2023 г.-24.12.2023 г.',
            'Показатели': [{'Массовая доля сорбиновой кислоты, мг/кг': ['90,2±10,0', 'не более 2000', True],
                            'Массовая доля бензойной кислоты, мг/кг': ['<20', '-', False]}, {
                               'Токсичные элементы, мг/кг:': ['Токсичные элементы, мг/кг:',
                                                              'Токсичные элементы, мг/кг:', '-'],
                               '- свинец': ['0,140±0,042', 'не более 0,35', True],
                               '- мышьяк': ['<0,05', 'не более 0,15', True],
                               '- кадмий': ['0,003±0,001', 'не более 0,07', True],
                               '- ртуть': ['< 0,002', 'не более 0,015', True],
                               'Пестициды, мг/кг:': ['Пестициды, мг/кг:', 'Пестициды, мг/кг:', '-'],
                               '- ГХЦГ(а, р, у - изомеры)': ['<0,01', 'не более 0,5', True],
                               '- ДДТ и его метаболиты': ['<0,01', 'не более 0,02', True],
                               '-гексахлорбензол': ['<0,01', 'не более 0,01', True],
                               '- ртутьорганические': ['<0,01', 'не допускаются', True],
                               '- 2,4-Д кислота, ее соли, эфиры': ['<0,02', 'не допускаются', True]}],
            'Нарушения норм': 'Не соответствуют'}


@pytest.fixture
def data_from_db_3():
    return {'Номер протокола': '№13509/23-Д', 'Дата протокола': '29 декабря 2023',
            'Место отбора проб': 77029,
            'Дата и время отбора проб': '19.12.2023 г., 08 ч. 55 мин.',
            'Сопроводительные документы': 'Акт отбора проб № 13509 от 19.12.2023 г.',
            'Группа продукции': 'Производство магазина',
            'Наименование продукции': 'Улитка греческая косичка с сыром и картофелем',
            'Дата производства продукции': '19.12.2023 г. Срок годности 24 часа',
            'Производитель (фирма, предприятие, организация)': 'АО «Дикси ЮГ»',
            'Дата проведения исследований': '19.12.2023 г.-25.12.2023 г.', 'Показатели': [
            {'Массовая доля сорбиновой кислоты, мг/кг': ['<20', 'не более 2000', True],
             'Массовая доля бензойной кислоты, мг/кг': ['<20', '-', False]},
            {'Токсичные элементы, мг/кг:': ['Токсичные элементы, мг/кг:', 'Токсичные элементы, мг/кг:', '-'],
             '- свинец': ['0,048±0,019', 'не более 0,35', True], '- мышьяк': ['<0,05', 'не более 0,15', True],
             '- кадмий': ['0,011±0,004', 'не более 0,07', True], '- ртуть': ['< 0,002', 'не более 0,015', True],
             'Пестициды, мг/кг:': ['Пестициды, мг/кг:', 'Пестициды, мг/кг:', '-'],
             '- ГХЦГ(а, Р, у - изомеры)': ['<0,01', 'не более 0,5', True],
             '- ДДТ и его метаболиты': ['<0,01', 'не более 0,02', True],
             '- гексахлорбензол': ['<0,01', 'не более 0,01', True],
             '- ртутьорганические': ['<0,01', 'не допускаются', True],
             '- 2,4-Д кислота, ее соли, эфиры': ['<0,02', 'не допускаются', True]}],
            'Нарушения норм': 'Не соответствуют'}
