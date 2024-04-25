# Импорт необходимых модулей
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd

from get_data_from_word_file import get_data_from_word_file


PATH_XLSX_STORES = r'C:\Users\RIMinullin\PycharmProjects\protocols\info6.xlsx'
DOC = 'C:\\Users\\RIMinullin\\Desktop\\для ворда\\большие\\32002 19.09.2023.docx'


KEYS_FOR_MAPPING_MODEL_PROTOCOL = {
    'Номер протокола': 'number',
    'Дата протокола': 'date',
    'Место отбора проб': 'store_id',
    'Дата и время отбора проб': 'sampling_datetime',
    'Сопроводительные документы': 'accompanying_documents',
    'Группа продукции': 'product_type',
    'Наименование продукции': 'name_of_product',
    'Дата производства продукции': 'production_date',
    'Производитель (фирма, предприятие, организация)': 'manufacturer',
    'Дата проведения исследований': 'date_of_test',
    'Показатели': 'indicators'
}

# Создание базы данных SQLite и настройка сессии
engine = create_engine('sqlite:///store.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Store(Base):
    """Модель - магазины"""
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, nullable=False)  # Уникальный номер магазина
    address = Column(String, nullable=False)  # Адрес магазина

    def __repr__(self):
        return f"<Магазин(номер={self.id}, адрес='{self.address}')>"


class Protocol(Base):
    """Модель - протоколы"""
    __tablename__ = 'protocols'

    number = Column(String, primary_key=True, nullable=False)
    date = Column(String, primary_key=True, nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'))
    sampling_datetime = Column(String, nullable=True)
    accompanying_documents = Column(String, nullable=True)
    product_type = Column(String, nullable=True)
    name_of_product = Column(String, nullable=True)
    production_date = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    date_of_test = Column(String, nullable=True)
    indicators = Column(JSON)

    def __repr__(self):
        return (
            f"<Номер протокола={self.number}, "
            f"Дата протокола='{self.date}, "
            f"Место отбора проб={self.sampling_site}, "
            f"Сопроводительные документы='{self.accompanying_documents}, "
            f"Группа продукции='{self.product_type}, "
            f"Наименование продукции='{self.name_of_product}, "
            f"Дата производства продукции='{self.production_date}, "
            f"Производитель (фирма, предприятие, организация)='{self.manufacturer}, "
            f"Дата проведения исследований='{self.date_of_test}, "
            f"Показатели='{self.indicators}, "
            f"')>"
        )


# Функция для создания таблицы в базе данных
def create_table():
    Base.metadata.create_all(engine)


# Функция для добавления магазина
def add_store(id, address):
    new_store = Store(id=id, address=address)
    session.add(new_store)
    session.commit()


# Забрать все магазины из БД
def list_stores():
    stores = session.query(Store).all()
    return stores


# Забрать все магазины из БД
def list_protocols():
    protocols = session.query(Protocol).all()
    return protocols


# Функция для удаления всех записей из таблицы магазинов
def clear_stores_table():
    # Очистка таблицы 'stores' от всех записей
    session.query(Store).delete()
    # Подтверждение изменений
    session.commit()


# Функция для удаления всех записей из таблицы магазинов
def clear_protocols_table():
    # Очистка таблицы 'stores' от всех записей
    session.query(Protocol).delete()
    # Подтверждение изменений
    session.commit()


def fill_the_stores(path_excel: str):
    df = pd.read_excel(path_excel)
    for _, row in df.iterrows():
        add_store(row['№ Магазина'], row['Адрес'])


def prepare_data_for_add_protocol(data: dict, dict_of_mapping: dict) -> dict:
    new_data = {}
    for i in data:
        new_data[dict_of_mapping[i]] = data[i]
    return new_data


# Функция для добавления протокола в БД.
def add_protocol(**kwargs):
    new_protocol = Protocol(**kwargs)
    session.add(new_protocol)
    session.commit()


def add_protocol_to_db(word_file: str) -> None:
    word_data = get_data_from_word_file(word_file)
    data_for_db = prepare_data_for_add_protocol(word_data, KEYS_FOR_MAPPING_MODEL_PROTOCOL)
    add_protocol(**data_for_db)


def view_all_tables_in_db():
    """Отобразить все таблицы и поля, находящиеся в БД."""
    metadata = MetaData()
    metadata.reflect(bind=engine)
    print(metadata.tables)


def drop_table(table_name, database_url):
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



# Base.metadata.create_all(engine)
database_url = 'sqlite:///store.db'


if __name__ == "__main__":

    # drop_table('protocols', database_url)
    # Создание таблицы
    # clear_protocols_table()
    # view_all_tables_in_db()
    # create_table()
    # add_protocol_to_db(DOC)
    print('list', list_protocols())
    # clear_stores_table()
    # Добавление примеров магазинов (закомментировано, чтобы не добавлять каждый раз при запуске)
    # add_store(32002, 'Брянская область, г. Клинцы, проспект Ленина, д.34')
    # add_store(2, 'Улица Советская, д. 25')
    # fill_the_stores(PATH_INFO6)
    # # Вывод всех магазинов
    # print(list_stores())

