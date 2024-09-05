""" Модуль с кодом для создания объектов моделей.

Функции:
    - Создание объектов, соответствующей модели:
    - create_main_protocol
    - create_manuf_prod
    - create_store_prod
    - create_air
    - create_water
    - create_washings
    - create_prod_control

    - split_code_and_address:
        Разбить место отбора проб на адрес и код магазина
    - create_date:
        Строку с датой преобразовать в объект datetime.

    - create_common_violations: сделать и вернуть вывод
    о наличии нарушений нормам для всей таблицы.

    - create_objects: получает на вход объект класса MainCollector,
    содержащий все данные, собранные с файла формата .docx.
    Обрабатывает их и возвращает структуру данных:
    Dict[Tuple[int, str], Union[MainProtocol, ManufProd, ProdControl,
                                Air, Water, Washings, StoreProd]]

Пример использования:
    - objects_for_db = create_objects(main_collector)

"""
import re
import sys
from pathlib import Path
from typing import Dict, Tuple, Union, List
from datetime import datetime, date

from league_sert.data_preparation.file_parser import MainCollector
from league_sert.exceptions import TypeIndicatorsError
from league_sert.models.exceptions import AttrNotFoundError

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from league_sert.models.models import (MainProtocol, ManufProd, Air, Water,
                                       ProdControl, Washings, StoreProd)


def create_common_violations(table_data: dict) -> List[bool]:
    """Вернуть вывод о наличии нарушений результатов
    нормам для всей таблицы целиком.
    :param table_data: Словарь с данными по одной таблиц показателей.
    :return: Список булевых значений, где каждое значение указывает
    на наличие или отсутствие нарушений для показателей всей таблицы. """

    if isinstance(table_data['indicators'], list):
        main_viol = False
        deviation_viol = False
        for sub_table in table_data['indicators']:
            if sub_table['violations_of_norms'][0]:
                main_viol = True
            if sub_table['violations_of_norms'][1]:
                deviation_viol = True
        return [main_viol, deviation_viol]
    raise TypeIndicatorsError()


def split_code_and_address(text: str) -> tuple[str, int]:
    """ Разбить место отбора проб на адрес и код магазина. """
    pattern = r'(.+)\(№?\s*(\d+)|(\d{5})(.*)'
    match = re.search(pattern, text)
    if match:
        if match.group(1):
            address = match.group(1).strip(', ()')
            code = int(match.group(2))
        else:
            address = match.group(4).strip(', ()')
            code = int(match.group(3))
        return address, code
    raise Exception(f'Не найден адрес {text}')


def create_date(date_: str) -> date:
    """ Строку с датой преобразовать в объект datetime. """
    months = {
        'января': '1',
        'февраля': '2',
        'марта': '3',
        'апреля': '4',
        'мая': '5',
        'июня': '6',
        'июля': '7',
        'августа': '8',
        'сентября': '9',
        'октября': '10',
        'ноября': '11',
        'декабря': '12',
    }
    date_ = re.sub(r'\s{2,}', ' ', date_)
    pattern = r'\d{2}.\d{2}.\d{2,4}'
    match = re.search(pattern, date_)
    if not match:
        date_ = date_.split(' ')
        if len(date_) < 3:
            raise ValueError('Некорректный формат даты.')
        date_[1] = months[date_[1]]
        date_ = '.'.join(date_[:3])
    else:
        date_ = match.group()

    date_ = datetime.strptime(date_, '%d.%m.%Y')
    return date_.date()


def validate_attribute(class_name, value, attr_name):
    """ Проверить, что атрибут не None и не пустая строка. """
    if value is None or value == '':
        raise AttrNotFoundError(class_name, attr_name)


def create_main_protocol(main_number, main_date, table_data: dict):
    """ Создать объект модели MainProtocol.  """
    address, code = split_code_and_address(table_data['Место отбора проб'])
    main_date = create_date(main_date)
    sampling_date = create_date(table_data['Дата и время отбора проб'])

    validate_attribute(MainProtocol, main_number, 'main_number')
    validate_attribute(MainProtocol, main_date, 'main_date')
    validate_attribute(MainProtocol, code, 'code')

    return MainProtocol(
        number=main_number,
        date=main_date,
        store_code=code,
        sampling_date=sampling_date,
        store_address=address)


def create_prod_control(**kwargs):
    """ Создать объект модели ProdControl.  """
    return ProdControl(
        number=kwargs['number_of_protocol'],
        date=create_date(kwargs['date_of_protocol']),
        act=kwargs['act'],
        address=kwargs['place_of_measurement'],
        conclusion=kwargs['inner_conclusion'],
        conclusion_compl=True if kwargs['inner_conclusion'] else False,
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        parameter=kwargs['parameter'],
        unit=kwargs['unit'])


def create_manuf_prod(**kwargs):
    """ Создать объект модели ManufProd.  """
    return ManufProd(
        sample_code=kwargs['Шифр пробы'],
        prod_name=kwargs['Наименование продукции'],
        prod_date=kwargs['Дата производства продукции'],
        manuf=kwargs['Производитель (фирма, предприятие, организация)'],

        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc'])


def create_store_prod(**kwargs):
    """ Создать объект модели ManufProd.  """
    return StoreProd(
        sample_code=kwargs['Шифр пробы'],
        prod_name=kwargs['Наименование продукции'],
        prod_date=create_date(kwargs['Дата производства продукции']),
        manuf=kwargs['Производитель (фирма, предприятие, организация)'],
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc'])


def create_air(**kwargs):
    """ Создать объект модели Air. """
    validate_attribute(Air, kwargs['name_indic'], 'name_indic')

    return Air(
        sample_code=kwargs['Шифр пробы'],
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc'])


def create_water(**kwargs):
    """ Создать объект модели Water.  """
    return Water(
        test_object=kwargs['Объект исследований'],
        sample_code=kwargs['Шифр пробы'],
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc'])


def create_washings(**kwargs):
    """ Создать объект модели Water.  """
    return Washings(
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc_of_method'])


ObjectsForDB = Dict[Tuple[int, str], Union[
    MainProtocol, ManufProd, ProdControl, Air, Water, Washings, StoreProd]]


def create_objects_same_cls(table_data: dict, type_table):
    """ Создание объектов одного и того же класса, в результате будет создан
    объект класса на каждый показатель. """

    methods = {
        'manuf_prod': create_manuf_prod,
        'store_prod': create_store_prod,
        'air': create_air,
        'water': create_water,
        'washings': create_washings,
        'PROD_CONTROL': create_prod_control}

    result = []
    method = methods.get(type_table, None)
    indicators = table_data['indicators']
    del table_data['indicators']
    for row in indicators:
        for name_indic, value in row.items():
            result.append(method(name_indic=name_indic, **table_data, **value))
    return result


def create_all_objects(main_collector: MainCollector) -> ObjectsForDB:
    """ Создание из объекта класса MainCollector, содержащего все данные из
     файла, набора объектов всех моделей. """

    objects_of_models = {}
    for key, value in main_collector.data_from_tables.items():
        if key[1] == 'MAIN':
            objects_of_models[key] = create_main_protocol(main_collector.main_number,
                                                          main_collector.main_date,
                                                          value)
        else:
            objects_of_models[key] = create_objects_same_cls(value, key[1])
    return objects_of_models