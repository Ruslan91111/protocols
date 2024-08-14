""" Тестирование модуля merge_tables. """

from league_sert.data_preparation.merge_tables import (join_sample_and_results,
                                                       remove_results_table,
                                                       refine_and_merge_tables)

data_input = {
    (0, 'MAIN'): {
        'Место отбора проб': 'Ленинградская область, Гатчинский р-н, г. Гатчина, '
                             ''
                             'ул. Куприна, д. 48, л. А (№47109)',
        'Дата и время отбора проб': '02.05.2024 г., 16 ч. 40 мин.'},
    (1, 'SAMPLE'): {'Шифр пробы': '4225-1', 'Группа продукции': 'Продукция производителя',
                    'Наименование продукции': 'Консервы. Оливки фаршированные лимоном',
                    'НД на продукцию': '-',
                    'Дата производства продукции': '27.07.2023 г. Годен до 27.07.2026 г.',
                    'Производитель (фирма, предприятие, организация)':
                        'La Roda de Andalucia'},
    (2, 'RESULTS'): [['Показатели', 'Результат измерений', 'Требования НД',
                      'НД на методы испытаний'],
                     ['Неспорообразующие микроорганизмы, плесневые грибы и дрожжи',
                      'не обнаружено в 1 г (см³)',
                      'не допускаются в 1 г (см³)', 'ГОСТ 30425-97']],
    (3, 'SAMPLE'): {'Шифр пробы': '4225-2', 'Группа продукции': 'Продукция производителя',
                    'Наименование продукции': 'Салака х/к',
                    'НД на продукцию': 'ТУ 10.20.24-129-00472093-2017',
                    'Дата производства продукции': '09.04.2024 г. Годен до 08.06.2024 г.',
                    'Производитель (фирма, предприятие, организация)': 'ИП Мачехин В.Я.'},
    (4, 'RESULTS'): [['Наименованиепоказателя', 'Результат',
                      'ТребованияНД', 'НД на методы испытаний'],
                     ['БГКП (колиформы)', 'не обнаружены в 0,1 г',
                      'не допускаются в 0,1 г', 'ГОСТ 31747-2012']],
    (5, 'SAMPLE'): {'Шифр пробы': '4225-3', 'Группа продукции': 'Продукция производителя',
                    'Наименование продукции': 'Масло сладко-сливочное несоленое м.д. жира 82,5 %',
                    'НД на продукцию': 'ГОСТ 32261-2013',
                    'Дата производства продукции': '23.03.2024 г. Годен до 22.05.2024 г.',
                    'Производитель (фирма, предприятие, организация)':
                        'ОАО «Озерецкий молочный комбинат»'},
    (6, 'RESULTS'): [
        ['Наименование показателя', 'Результат', 'Требования НДМУ 4.1./4.2.2484-09ГОСТ Р 52253-04',
         'НД на методы испытаний'],
        ['Массовая доля масляной кислоты (Сдд), %', '3,2±0,4', '2,0-4,2',
         'ГОСТ 32915-2014']],
    (7, 'RESULTS'): [['Наименование показателя', 'Результат', 'Требования нд',
                      'НД на методы испытаний'],
                     ['Количество мезофильных, аэробных и факультативно-анаэробных '
                      'микроорганизмов, КОЕ/г', '8,5х10³',
                      'не более 1,0x10⁵', 'ГОСТ 32901-14']],
    (8, 'SAMPLE'): {'Шифр пробы': '4225-4', 'Группа продукции': 'Продукция производителя',
                    'Наименование продукции': 'Филе ЦБ. Полуфабрикат из мяса птицы',
                    'НД на продукцию': 'СТО 0058187-018-2016',
                    'Дата производства продукции': '30.04.2024 г. Годен до 07.05.2024 г.',
                    'Производитель (фирма, предприятие, организация)':
                        'АО «ПРОДО Птицефабрика Калужская»'},
    (9, 'RESULTS'): [['Наименование показателя', 'Результат', 'Требования нд',
                      'НД на методы испытаний'],
                     ['Количество мезофильных, аэробных и факультативно-анаэробных'
                      ' микроорганизмов, КОЕ/г', '2,0x10⁴',
                      'не более 1,0x10⁵', 'ГОСТ 10444.15-94']],
    (10, 'SAMPLE'): {'Объект исследования': 'Воздух (микробная обсемененность)'},
    (11, 'RESULTS'): [
        ['№ п/п', 'Место отбора пробы', 'Наименованиепоказателя', 'Результат', 'Требования нд',
         'НД на методы исследований'],
        ['1', 'Холодильная камера «Молочные продукты»', 'Плесени,КОЕ на чашке',
         '0', '', 'СП 4695-88']],
    (13, 'PROD_CONTROL'): [
        ['№ п/п', 'Место измерений, наименование рабочего места',
         'Измеряемый параметр', 'Измеряемый параметр',
         'Единицы измерений', 'Результат измерения*', 'Допустимое значение (ПДУ, ПДК)']]}


def test_join_sample_and_results():
    """ Тестируется правильное объединение таблиц с образцами и результатами исследований. """
    result_tables = join_sample_and_results(data_input)
    assert result_tables[(1, 'SAMPLE')]['indicators'] == [(data_input[(2, 'RESULTS')])]
    assert result_tables[(3, 'SAMPLE')]['indicators'] == [(data_input[(4, 'RESULTS')])]
    assert result_tables[(5, 'SAMPLE')]['indicators'] == [(data_input[(6, 'RESULTS')]),
                                                          (data_input[(7, 'RESULTS')])]


def test_remove_results_table():
    """ Тестируется удаление таблиц с результатами
    исследований после их добавления в поле indicators."""
    tables = join_sample_and_results(data_input)
    result_tables = remove_results_table(tables)
    result_keys = {i[1] for i in result_tables.keys()}
    assert 'RESULTS' not in result_keys


def test_refine_and_merge_tables():
    """ Протестировать работу функции по объединению
    и присвоению наименования вида таблицы"""
    result_data = refine_and_merge_tables(data_input)
    assert list(result_data.keys()) == [
        (0, 'MAIN'), (1, 'manuf_prod'), (3, 'manuf_prod'), (5, 'manuf_prod'), (8, 'manuf_prod'),
        (10, 'air'), (13, 'PROD_CONTROL')
    ]