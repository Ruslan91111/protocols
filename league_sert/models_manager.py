""" Модуль с кодом для создания объектов моделей. """

import sys
from pathlib import Path

from league_sert.data_preparation.file_parser import MainCollector
from league_sert.exceptions import WrongNameOfTableError

BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from league_sert.models import MainProtocol, ManufProd, Air, Water, ProdControl


def process_violations(table_data: dict):
    """Вернуть вывод о наличии нарушений результатов нормам для всей таблицы целиком."""
    if isinstance(table_data['indicators'], list):
        main_viol = False
        deviation_viol = False
        for sub_table in table_data['indicators']:
            if sub_table['violations_of_norms'][0]:
                main_viol = True
            if sub_table['violations_of_norms'][1]:
                deviation_viol = True
        return main_viol, deviation_viol


def create_main_protocol(main_number, main_date, table_data: dict):
    """ Создать объект модели MainProtocol.  """
    return MainProtocol(number=main_number,
                        date=main_date,
                        sampling_site=table_data['Место отбора проб'],
                        sampling_date=table_data['Дата и время отбора проб'])


def create_manuf_prod(table_data: dict):
    """ Создать объект модели ManufProd.  """
    return ManufProd(sample_code=table_data['Шифр пробы'],
                     prod_name=table_data['Наименование продукции'],
                     prod_date=table_data['Дата производства продукции'],
                     manuf=table_data['Производитель (фирма, предприятие, организация)'],
                     indic=table_data['indicators'],
                     indic_compl=process_violations(table_data))


def create_air(table_data: dict):
    """ Создать объект модели Air.  """
    return Air(sample_code=table_data['Шифр пробы'],
               indic=table_data['indicators'],
               indic_compl=process_violations(table_data))


def create_water(table_data: dict):
    """ Создать объект модели Water.  """
    return Water(test_object=table_data['Объект исследований'],
                 indic=table_data['indicators'],
                 sample_code=table_data['Шифр пробы'],
                 indic_compl=process_violations(table_data))


def create_prod_control(**kwargs):
    """ Создать объект модели ProdControl.  """
    return ProdControl(number=kwargs['number_of_protocol'],
                       date=kwargs['date_of_protocol'],
                       act=kwargs['act'],
                       address=kwargs['place_of_measurement'],
                       indic=kwargs['indicators'],
                       indic_compl=process_violations(kwargs),
                       conclusion=kwargs['inner_conclusion'],
                       conclusion_compl=True if kwargs['inner_conclusion'] else False)


def create_all_objects(main_collector: MainCollector):
    """ Создание из данных объекта класса MainCollector набора моделей. """

    objects_of_models = {}

    for key, value in main_collector.data_from_tables.items():
        if key[1] == 'MAIN':
            objects_of_models[key] = create_main_protocol(main_collector.main_number, main_collector.main_date, value)
        elif key[1] == 'manuf_prod':
            objects_of_models[key] = create_manuf_prod(value)
        elif key[1] == 'air':
            objects_of_models[key] = create_air(value)
        elif key[1] == 'water':
            objects_of_models[key] = create_water(value)
        elif key[1] == 'PROD_CONTROL':
            objects_of_models[key] = create_prod_control(**main_collector.prod_control_data,
                                                         indicators=value)
        else:
            raise WrongNameOfTableError()

    return objects_of_models
