import json
import os

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy.exc import IntegrityError

from get_data_from_word_file import get_all_data_from_word_file


PATH_XLSX_STORES = r'C:\Users\RIMinullin\PycharmProjects\protocols\info6.xlsx'
DOC = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\большие\\32002 19.09.2023.docx'
# Base.metadata.create_all(engine)
DATABASE_URL = 'sqlite:///store.db'
DIR_WITH_WORD = r'C:\\Users\\RIMinullin\\Desktop\\для ворда\\большие\\'

# Словарь для сопоставления ключей из данных, собранных в word документе
# и наименований полей в модели Protocol
KEYS_FOR_MAPPING_MODEL_PROTOCOL = {
    'Номер протокола': 'number',
    'Дата протокола': 'date',
    'Место отбора проб': 'store_id',
    'Адрес магазина': 'address',
    'Дата и время отбора проб': 'sampling_datetime',
    'Сопроводительные документы': 'accompanying_documents',
    'Группа продукции': 'product_type',
    'Наименование продукции': 'name_of_product',
    'Дата производства продукции': 'production_date',
    'Производитель (фирма, предприятие, организация)': 'manufacturer',
    'Дата проведения исследований': 'date_of_test',
    'Показатели': 'indicators'
}

# Создание базы данных SQLite и настройка сессии.
# echo - параметр для вывода операций с БД в консоль.
engine = create_engine('sqlite:///store.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


#############################################################################
# МОДЕЛИ - ДАННЫХ
#############################################################################
class Base(DeclarativeBase):
    """ Базовый класс для создания и наследования нашими моделями """
    pass


class Store(Base):
    """Модель - магазины"""
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, nullable=False)  # Уникальный номер магазина
    address = Column(String, nullable=False)  # Адрес магазина
    # Связь с таблицей протоколы
    protocols = relationship("Protocol", back_populates="store")

    def __repr__(self):
        """Представление экземпляров класса"""
        return f"<Магазин(номер={self.id}, адрес='{self.address}')>"


class Protocol(Base):
    """Модель - протоколы"""
    __tablename__ = 'protocols'
    # Primary key - составной на два поля.
    number = Column(String, primary_key=True, nullable=False)
    date = Column(String, primary_key=True, nullable=False)
    # Foreign Key - store - связь с таблицей магазины
    store_id = Column(Integer, ForeignKey('stores.id'))
    store = relationship("Store", back_populates="protocols")

    sampling_datetime = Column(String, nullable=True)
    accompanying_documents = Column(String, nullable=True)
    product_type = Column(String, nullable=True)
    name_of_product = Column(String, nullable=True)
    production_date = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    date_of_test = Column(String, nullable=True)
    indicators = Column(JSON)

    def __repr__(self):
        """Представление экземпляров класса"""
        return (
            f"<Номер протокола={self.number}, "
            f"Дата протокола='{self.date}, "
            f"Место отбора проб={self.store_id}, "
            f"Сопроводительные документы='{self.accompanying_documents}, "
            f"Группа продукции='{self.product_type}, "
            f"Наименование продукции='{self.name_of_product}, "
            f"Дата производства продукции='{self.production_date}, "
            f"Производитель (фирма, предприятие, организация)='{self.manufacturer}, "
            f"Дата проведения исследований='{self.date_of_test}, "
            f"Показатели='{self.indicators}, "
            f"')>"
        )


#############################################################################
# КЛАССЫ - ДЛЯ ВЗАИМОДЕЙСТВИЯ С МОДЕЛЯМИ.
#############################################################################
class StoreManager:
    """ Класс для взаимодействия с моделью Store."""

    def add_store_to_db(self, id, address):
        """ Добавить в таблицу экземпляр магазина. """
        new_store = Store(id=id, address=address)
        session.add(new_store)
        # Подтверждение изменений
        session.commit()

    def fill_the_stores_from_file(self, path_excel: str):
        """ Заполнить таблицу данными из xlsx файла,
        содержащего коды и адреса магазинов. """
        df = pd.read_excel(path_excel)
        for _, row in df.iterrows():
            self.add_store_to_db(row['№ Магазина'], row['Адрес'])

    def get_all_stores(self) -> list:
        """ Забрать все магазины из БД. """
        stores = session.query(Store).all()
        return stores

    def delete_all_stores_from_table(self):
        """Функция для удаления всех записей из таблицы магазинов"""
        session.query(Store).delete()
        session.commit()


class ProtocolManager:
    """ Класс для взаимодействия с моделью Protocol."""

    def add_protocol_to_db(self, word_file: str) -> None:
        """ Добавить экземпляр протокола в таблицу БД. """

        def _prepare_data_for_add_protocol(data: dict, dict_of_mapping: dict) -> dict:
            """Внутренняя функция - заменить ключи в данных, подготовленных для
            записи в БД на наименования полей модели."""
            new_data = {}
            for i in data:
                new_data[dict_of_mapping[i]] = data[i]
            return new_data

        Session = sessionmaker(bind=engine)
        session = Session()
        # Получить данные для добавления в таблицу из word файла.
        word_data = get_all_data_from_word_file(word_file)
        # Подготовить данные для добавления
        data_for_db = _prepare_data_for_add_protocol(word_data, KEYS_FOR_MAPPING_MODEL_PROTOCOL)
        # Записываем экземпляр в таблицу.
        new_protocol = Protocol(**data_for_db)
        session.add(new_protocol)
        session.commit()

    def get_all_protocols(self) -> list:
        """ Забрать все протоколы из БД. """
        protocols = session.query(Protocol).all()
        return protocols

    def delete_all_protocols_from_table(self):
        """Функция для удаления всех записей из таблицы протоколов."""
        session.query(Protocol).delete()
        session.commit()


#############################################################################
# Функции
#############################################################################
def create_table():
    """ Создать в БД все таблицы, описанные в модуле. """
    Base.metadata.create_all(engine)


def get_all_tables_in_db():
    """Вернуть все таблицы и поля, находящиеся в БД."""
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata.tables


def drop_the_table_in_db(table_name, database_url):
    """Удалить таблицу из БД."""
    engine = create_engine(database_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Проверяем, существует ли таблица
    if table_name in metadata.tables:
        table = Table(table_name, metadata, autoload=True, autoload_with=engine)
        table.drop(engine)
        print(f"Таблица '{table_name}' успешно удалена.")
    else:
        print(f"Таблица '{table_name}' не найдена в базе данных.")


def apply_func_through_for(path_to_dir: str, func):
    """ Применить одну из функций модуля через цикл ко всем документам в директории. """
    # Множество из имен word файлов в папке.
    word_files = {i for i in os.listdir(path_to_dir) if i[0] != '~' and i[-5:] == '.docx'}
    for file in word_files:
        filename = path_to_dir + file

        print('Название файла: ', file)
        try:
            func(filename)
        except IntegrityError:
            print(f'File {file}, не записан в БД, объект уже существует в таблице.')


def launch_write_protocols_to_db():
    apply_func_through_for(DIR_WITH_WORD, ProtocolManager().add_protocol_to_db)


def protocols_from_db_to_excel():
    all_protocols = ProtocolManager().get_all_protocols()

    # Загружаем данные из таблицы в DataFrame
    df = pd.read_sql_table('protocols', engine)

    # Преобразуем столбец indicators с JSON данными в отдельные столбцы
    df['indicators'] = df['indicators'].apply(lambda x: json.loads(x))

    # Загружаем данные из таблицы stores для получения названия магазина
    df_stores = pd.read_sql_table('stores', engine)

    # Объединяем данные из двух таблиц по столбцу store_id
    df = pd.merge(df, df_stores[['id', 'address']], left_on='store_id', right_on='id', how='left')
    df = df.drop('id', axis=1)  # Удаляем лишний столбец с id

    df = df[[col for col in KEYS_FOR_MAPPING_MODEL_PROTOCOL.values()]]

    df.columns = list(KEYS_FOR_MAPPING_MODEL_PROTOCOL.keys())
    # Сохраняем данные в Excel файл
    df.to_excel('название_файла.xlsx', index=False)


if __name__ == "__main__":
    # launch_write_protocols_to_db()
    protocols_from_db_to_excel()

    # Удалить полностью таблицу из БД
    # drop_the_table_in_db('protocols', DATABASE_URL)
    # drop_the_table_in_db('stores', DATABASE_URL)

    # Создать все таблицы, описанные в модуле
    # create_table()

    # Просмотреть все таблицы в БД
    # print(get_all_tables_in_db())

    # Добавить конкретный протокол в таблицу
    # ProtocolManager().add_protocol_to_db(DOC)

    # Добавление конкретного магазина
    # StoreManager().add_store_to_db(32002, 'Брянская область, г. Клинцы, проспект Ленина, д.34')

    # Заполнить таблицу всеми магазинами в файле.
    # StoreManager().fill_the_stores_from_file(PATH_XLSX_STORES)

    # all_protocols = ProtocolManager().get_all_protocols()
    # all_stores = StoreManager().get_all_stores()
    # print(all_stores)
