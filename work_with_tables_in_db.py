import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, joinedload

from constants import KEYS_FOR_MAPPING_MODEL_PROTOCOL, DATABASE_URL
from models import Base, Store, Protocol


# Создание базы данных SQLite и настройка сессии.
engine = create_engine('sqlite:///store.db', echo=True)
Session = sessionmaker(bind=engine)


class DataBaseWorker:
    """ Класс для общих манипуляций с БД и таблицами в ней."""
    def __init__(self, base=Base):
        self.base = Base
        self.metadata = MetaData()

    def create_all_tables(self):
        """ Создать в БД все таблицы, описанные в модуле. """
        self.base.metadata.create_all(engine)

    def get_all_tables_from_db(self):
        """Вернуть все таблицы и поля, находящиеся в БД."""
        self.metadata.reflect(bind=engine)
        return self.metadata.tables

    def drop_the_table_in_db(self, table_name, database_url):
        """Удалить таблицу из БД."""
        engine = create_engine(database_url)
        self.metadata.reflect(bind=engine)

        # Проверяем, существует ли таблица
        if table_name in self.metadata.tables:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=engine)
            table.drop(engine)
            print(f"Таблица '{table_name}' успешно удалена.")
        else:
            print(f"Таблица '{table_name}' не найдена в базе данных.")


class StoreManager:
    """ Класс для взаимодействия с моделью Store."""
    def __init__(self, Session):
        self.session = Session

    def add_store_to_db(self, id, address):
        """Добавить в таблицу экземпляр магазина."""
        session = self.session()
        try:
            new_store = Store(id=id, address=address)
            session.add(new_store)
            session.commit()  # Подтверждение изменений
        except Exception as e:
            session.rollback()  # Откат изменений в случае ошибки
            print(f"Ошибка при добавлении магазина: {id} - {e}")
        finally:
            session.close()  # Закрытие сессии

    def fill_the_stores_from_file(self, path_excel: str):
        """Заполнить таблицу данными из xlsx файла,
        содержащего коды и адреса магазинов."""
        df = pd.read_excel(path_excel)
        for _, row in df.iterrows():
            self.add_store_to_db(row['№ Магазина'], row['Адрес'])

    def get_all_stores(self) -> list:
        """Забрать все магазины из БД."""
        session = self.session()
        try:
            stores = session.query(Store).all()
            return stores
        except Exception as e:
            print(f"Ошибка при получении магазинов: {e}")
        finally:
            session.close()

    def delete_all_stores_from_table(self):
        """ Удалить все записи из таблицы магазинов. """
        session = self.session()
        try:
            session.query(Store).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при удалении магазинов: {e}")
        finally:
            session.close()


class ProtocolManager:
    """Класс для взаимодействия с моделью Protocol."""
    def __init__(self, Session=Session):
        self.session = Session

    def add_protocol_to_db(self, protocol_data: dict) -> None:
        """Добавить экземпляр протокола в таблицу БД."""

        def _prepare_data_for_add_protocol(data: dict, dict_of_mapping: dict) -> dict:
            """Внутренняя функция - заменить ключи в данных, подготовленных для
            записи в БД на наименования полей модели."""
            new_data = {}
            for i in data:
                if i in dict_of_mapping:  # Проверьте, существует ли ключ в маппинге
                    new_data[dict_of_mapping[i]] = data[i]
            return new_data

        session = self.session()

        try:
            # Подготовить данные для добавления
            data_for_db = _prepare_data_for_add_protocol(protocol_data,
                                                         KEYS_FOR_MAPPING_MODEL_PROTOCOL)
            new_protocol = Protocol(**data_for_db)
            session.add(new_protocol)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении протокола:{protocol_data['Номер протокола']} - {e}")
        finally:
            session.close()

    def get_all_protocols(self) -> list:
        """Забрать все протоколы из БД."""
        session = self.session()
        try:
            protocols = session.query(Protocol).options(joinedload(Protocol.store)).all()
            return protocols
        except Exception as e:
            print(f"Ошибка при получении списка протоколов из БД: {e}")
        finally:
            session.close()

    def delete_all_protocols_from_table(self) -> None:
        """Функция для удаления всех записей из таблицы протоколов."""
        session = self.session()
        try:
            session.query(Protocol).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()




data = {'Номер протокола': '№13509/23-Д', 'Дата протокола': '29 декабря 2023', 'Место отбора проб': '77029',
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


if __name__ == "__main__":
    # database_worker = DataBaseWorker()
    # launch_write_protocols_to_db()
#     # protocols_from_db_to_excel()
#
#     # Удалить полностью таблицу из БД
#     database_worker.drop_the_table_in_db('protocols', DATABASE_URL)
#     # database_worker.drop_the_table_in_db('stores', DATABASE_URL)
#
#     # Создать все таблицы, описанные в модуле
#     database_worker.create_tables()
#
#     # Просмотреть все таблицы в БД
#     print(database_worker.get_all_tables_in_db())
#     all_protocols = ProtocolManager().get_all_protocols()
#     print(all_protocols)
#     ProtocolManager().delete_all_protocols_from_table()
#
#     # Добавить конкретный протокол в таблицу
    ProtocolManager().add_protocol_to_db(data)
    ProtocolManager().add_protocol_to_db(data)
#     ProtocolManager().add_protocol_to_db(WordFileParser(FILE_2).get_all_required_data_from_word_file())
#     all_protocols = ProtocolManager().get_all_protocols()
#     print(all_protocols)
#     print(len(all_protocols))
# #
#     # Добавление конкретного магазина
#     # StoreManager(session).add_store_to_db(32002, 'Брянская область, г. Клинцы, проспект Ленина, д.34')
#
#     # Заполнить таблицу всеми магазинами в файле.
#     # StoreManager().fill_the_stores_from_file(PATH_XLSX_STORES)
