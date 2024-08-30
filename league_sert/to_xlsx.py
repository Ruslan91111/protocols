"""
Модуль для записи данных из БД в xlsx файл.

def create_dataframe_from_a_protocol(protocol_data: Protocol) -> pd.DataFrame:
    Получить на вход объект протокол - одна строка из БД,
    преобразовать и вернуть DataFrame.

def write_protocols_from_db_in_xlsx_file(
        protocols_from_db: dict, name_of_result_file: str) -> None:
     Получить на вход список с объектами протоколов из БД, каждый объект
     преобразовать в pd.DataFrame, преобразовать в единый DataFrame
     и записать в xlsx файл.
"""
import time

import pandas as pd

from sqlalchemy.orm import joinedload
from database.db_config import prot_session_maker

from league_sert.models import (MainProtocol, ManufProd, Air, Water,
                                ProdControl, Washings, StoreProd)

cols = [
    'id основного протокола',
    'Номер основного протокола',
    'Дата основного протокола',
    'Место отбора проб',
    'Дата и время отбора проб',

    'Номер протокола произв контроля',
    'Дата протокола произв контроля',
    'Акт произв контроля',
    'Адрес измерений произв контроля',
    'Заключение произв контроля',
    'Нарушения в заключении произв контроля',
    'Соответствие нормам основных чисел произв контроля',
    'Соответствие нормам чисел с отклонением произв контроля',

    'Место измерения произв контроля',
    'Параметр произв контроля',
    'Единица измерений произв контроля',
    'Результат измерений произв контроля',
    'Нормы для показателей произв контроля',
    'Соответствие результата нормам произв контроля',
    'Соответствие результата с отклонением нормам произв контроля',

    'Шифр пробы продукция производства',
    'Наименование продукции производства',
    'Дата производства продукция производства',
    'Производитель',
    'Соответствие нормам основных чисел продукция производства',
    'Соответствие нормам чисел с отклонением продукция производства',

    'Показатель продукция производства',
    'Результат исследований продукция производства',
    'Нормы продукция производства',
    'Нормативные документы продукция производства',
    'Соответствие результата нормам продукция производства',
    'Соответствие результата нормам с отклонением продукция производства',

    'Шифр пробы производство магазина',
    'Наименование производство магазина',
    'Дата производства производство магазина',
    'Производитель производство магазина',
    'Соответствие нормам основных чисел производство магазина',
    'Соответствие нормам чисел с отклонением производство магазина',

    'Показатель производство магазина',
    'Результат исследований производство магазина',
    'Нормы производство магазина',
    'Нормативные документы производство магазина',
    'Соответствие результата нормам производство магазина',
    'Соответствие результата нормам с отклонением производство магазина',

    'Шифр пробы воздух',
    'Соответствие нормам основных чисел воздух',
    'Соответствие нормам чисел с отклонением воздух',

    'Показатель воздух',
    'Результат исследований воздух',
    'Нормы воздух',
    'Нормативные документы воздух',
    'Соответствие результата нормам чисел воздух',
    'Соответствие результата нормам с отклонением воздух'

    'Объект исследования вода',
    'Шифр пробы продукция вода',
    'Соответствие нормам основных чисел вода',
    'Соответствие нормам чисел с отклонением вода',

    'Показатель вода',
    'Результат исследований вода',
    'Нормы вода',
    'Нормативные документы',
    'Соответствие результат нормам вода',
    'Соответствие результата нормам с отклонением вода',

    'Объект исследования смывы',
    'Соответствие нормам основных чисел смывы',
    'Соответствие нормам чисел с отклонением смывы',

    'Показатель смывы',
    'Результат исследований смывы',
    'Нормы смывы',
    'Нормативные документы смывы',
    'Соответствие результата нормам смывы',
    'Соответствие результата нормам с отклонением смывы'

]


def get_all_protocols() -> list:
    """Забрать все данные из БД, выполнив join со всеми таблицами. """
    with prot_session_maker() as session:
        try:
            protocols = session.query(MainProtocol).options(
                joinedload(MainProtocol.manuf_prod),
                joinedload(MainProtocol.washings),
                joinedload(MainProtocol.air),
                joinedload(MainProtocol.water),
                joinedload(MainProtocol.prod_control),
                joinedload(MainProtocol.store_prod)
            ).all()
            return protocols
        except Exception as e:
            print(f"Ошибка при получении списка протоколов из БД: {e}")
        finally:
            session.close()


class ConverterToDict:
    """ Собрать данные из основного протокола и
    связанных с ним других моделей в единый словарь."""

    def __init__(self, main_protocol):
        self.main_protocol = main_protocol
        self.processed_data = {}
        self.sub_cls = None

    def get_attrs_from_sub_cls(self):
        """ Преобразовать атрибуты из атрибута - объекта другого класса."""
        for iter_, table in enumerate(self.sub_cls):
            for atr_, value in table.__dict__.items():
                if atr_ not in {'_sa_instance_state', 'main_prot_id', 'main_prot', 'id'}:
                    self.processed_data[f'{iter_}_{table.__class__.__name__}_{atr_}'] = value

    def collect_all_attrs(self):
        """ Перебрать и сохранить значения всех атрибутов объекта MainProtocol. """
        for attr_, attr_val in self.main_protocol.__dict__.items():
            if isinstance(attr_val, str) or isinstance(attr_val, int):
                self.processed_data[attr_] = attr_val
            else:
                if not attr_ == '_sa_instance_state':
                    self.sub_cls = attr_val
                    self.get_attrs_from_sub_cls()


class ConverterToDF:
    """ Собрать данные из основного протокола и связанных
    с ним других моделей в единый DataFrame."""

    def __init__(self, main_protocol):
        self.main_protocol = main_protocol
        self.result_df = self.main_protocol.to_df()

    def create_sub_df(self, name_attr):
        """ Создать DataFrame из связанной таблицы,
        Сохранить в атрибут. """
        if hasattr(self.main_protocol, name_attr):

            if len(getattr(self.main_protocol, name_attr)) >= 1:
                common_df = pd.DataFrame()
                for obj in getattr(self.main_protocol, name_attr):
                    obj_df = obj.to_df()
                    common_df = pd.concat([common_df, obj_df],
                                          axis=0, ignore_index=True)
            else:
                common_df = pd.DataFrame()

            setattr(self, name_attr + '_df', common_df)

    def create_common_df(self):
        sub_cls = ['prod_control', 'manuf_prod', 'store_prod', 'air', 'water', 'washings']
        for name in sub_cls:
            self.create_sub_df(name)

        self.result_df = pd.concat([
            self.result_df, self.prod_control_df, self.manuf_prod_df, self.store_prod_df,
            self.air_df, self.water_df, self.washings_df], axis=1)


def write_all_protocols_in_xlsx(db_data, xlsx_path: str):
    """ Записать все протоколы из БД в один xlsx файл."""
    result_df = pd.DataFrame(columns=cols)

    for protocol in db_data:

        # Создать DataFrame из главного протокола и его атрибутов
        protocol = ConverterToDF(protocol)
        protocol.create_common_df()
        sub_df = protocol.result_df

        # Добавляем отсутствующие колонки
        for col in result_df.columns:
            if col not in sub_df.columns:
                sub_df[col] = None

        # Меняем порядок колонок в соответствии с основным датафреймом
        sub_df = sub_df[result_df.columns]
        result_df = pd.concat([result_df, sub_df], axis=0)

    result_df.to_excel(xlsx_path, index=False)


if __name__ == '__main__':
    start = time.time()
    db_data = get_all_protocols()
    xlsx_path = r'output.xlsx'
    write_all_protocols_in_xlsx(db_data, xlsx_path)
    print(time.time() - start)
