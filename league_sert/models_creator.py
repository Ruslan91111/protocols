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

import sys
from pathlib import Path
from typing import Dict, Tuple, Union, List

from league_sert.data_preparation.file_parser import MainCollector
from league_sert.exceptions import WrongNameOfTableError, TypeIndicatorsError

BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from league_sert.models import (MainProtocol, ManufProd, Air, Water,
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


def create_main_protocol(main_number, main_date, table_data: dict):
    """ Создать объект модели MainProtocol.  """
    return MainProtocol(
        number=main_number,
        date=main_date,
        sampling_site=table_data['Место отбора проб'],
        sampling_date=table_data['Дата и время отбора проб']
    )


def create_prod_control(**kwargs):
    """ Создать объект модели ProdControl.  """
    # violations = create_common_violations(kwargs)
    return ProdControl(
        number=kwargs['number_of_protocol'],
        date=kwargs['date_of_protocol'],
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
        unit=kwargs['unit'],
        #
        # violat_main=violations[0],
        # violat_dev=violations[1],
    )


def create_manuf_prod(**kwargs):
    """ Создать объект модели ManufProd.  """
    # violations = create_common_violations(kwargs)
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
        norm_doc=kwargs['norm_doc'],

        # violat_main=violations[0],
        # violat_dev=violations[1]
    )


def create_store_prod(**kwargs):
    """ Создать объект модели ManufProd.  """
    # violations = create_common_violations(kwargs)
    return StoreProd(
        sample_code=kwargs['Шифр пробы'],
        prod_name=kwargs['Наименование продукции'],
        prod_date=kwargs['Дата производства продукции'],
        manuf=kwargs['Производитель (фирма, предприятие, организация)'],

        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc'],

        # violat_main=violations[0],
        # violat_dev=violations[1]
    )


def create_air(**kwargs):
    """ Создать объект модели Air.  """
    # violations = create_common_violations(kwargs)
    return Air(
        sample_code=kwargs['Шифр пробы'],
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc'],
        # violat_main=violations[0],
        # violat_dev=violations[1]
    )


def create_water(**kwargs):
    """ Создать объект модели Water.  """
    # violations = create_common_violations(kwargs)
    return Water(
        test_object=kwargs['Объект исследований'],
        sample_code=kwargs['Шифр пробы'],
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc'],
        # violat_main=violations[0],
        # violat_dev=violations[1]
    )


def create_washings(**kwargs):
    """ Создать объект модели Water.  """
    # violations = create_common_violations(kwargs)
    return Washings(
        name_indic=kwargs['name_indic'],
        result=kwargs['result'],
        norm=kwargs['norm'],
        conformity_main=kwargs['conformity_main'],
        conformity_deviation=kwargs.get('conformity_deviation', True),
        norm_doc=kwargs['norm_doc_of_method'],
        # violat_main=violations[0],
        # violat_dev=violations[1]
    )


ObjectsForDB = Dict[Tuple[int, str], Union[
    MainProtocol, ManufProd, ProdControl, Air, Water, Washings, StoreProd]]


def create_objects_same_cls(table_data: dict, type_table):
    methods = {
        'manuf_prod': create_manuf_prod,
        'store_prod': create_store_prod,
        'air': create_air,
        'water': create_water,
        'washings': create_washings,
        'PROD_CONTROL': create_prod_control,
    }
    result = []
    method = methods.get(type_table, None)
    indicators = table_data['indicators']
    del table_data['indicators']
    for row in indicators:
        for k, v in row.items():
            name_indic = k
            value = v

            result.append(method(name_indic=name_indic, **table_data, **value))
    return result


def create_objects(main_collector: MainCollector) -> ObjectsForDB:
    """ Создание из данных объекта класса MainCollector набора моделей.
     :param: main_collector: Объект класса MainCollector,
     содержащий все необходимые данные, собранные с файла .docx."""

    objects_of_models = {}
    for key, value in main_collector.data_from_tables.items():
        if key[1] == 'MAIN':
            objects_of_models[key] = create_main_protocol(main_collector.main_number,
                                                          main_collector.main_date,
                                                          value)


        else:
            objects_of_models[key] = create_objects_same_cls(value, key[1])

    return objects_of_models



