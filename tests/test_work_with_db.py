# from pytest_lazyfixture import lazy_fixture
from sqlalchemy.exc import IntegrityError

import pandas as pd
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import KEYS_FOR_MAPPING_MODEL_PROTOCOL
from models import Protocol, Store, Base
from work_with_db import ProtocolManager, StoreManager


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
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


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


def test_add_store_to_db(store_manager, test_session):
    """ Тест добавления магазина в базу данных. """
    store_manager.add_store_to_db(1, 'Тестовый адрес')
    store = test_session.query(Store).first()
    assert store is not None
    assert store.id == 1
    assert store.address == 'Тестовый адрес'


def test_add_store_to_db_already_exists(test_session):
    """ Тест добавления магазина в БД, когда магазин с таким id уже существует. """
    # Создаем магазин, добавляем в БД.
    store1 = Store(id=1, address="UniqueStore")
    test_session.add(store1)
    test_session.commit()

    # Пытаемся добавить магазин с таким же id.
    store2 = Store(id=1, address="UniqueStore")
    test_session.add(store2)

    # Проверяем, что возникает исключение
    with pytest.raises(IntegrityError):
        test_session.commit()


def test_fill_the_stores_from_file(store_manager, test_session):
    """ Тест заполнения таблицы stores из файла. """
    df = pd.DataFrame({'№ Магазина': [1, 2, 3], 'Адрес': ['Адрес 1', 'Адрес 2', 'Адрес 3']})
    path_excel = './test_stores.xlsx'
    df.to_excel(path_excel, index=False)
    store_manager.fill_the_stores_from_file(path_excel)
    stores = test_session.query(Store).all()
    assert len(stores) == 3
    assert stores[0].address == 'Адрес 1'
    assert stores[1].address == 'Адрес 2'
    assert stores[2].address == 'Адрес 3'


def test_delete_all_stores_from_table(store_manager, test_session):
    """ Тест удаления всех магазинов из базы данных. """
    store_manager.add_store_to_db(1, 'Адрес')
    store_manager.add_store_to_db(2, 'Другой адрес')
    store_manager.delete_all_stores_from_table()
    stores = test_session.query(Store).all()
    assert len(stores) == 0


@pytest.mark.parametrize("data_for_input, data_from_db",
                         [("data_from_word_file_1", "data_from_db_1"),
                          ("data_from_word_file_2", "data_from_db_2"),
                          ("data_from_word_file_3", "data_from_db_3")])
def test_add_protocol_to_db(request, protocol_manager, test_session, data_for_input, data_from_db):
    """ Тест добавления протокола в базу данных. """
    data_for_db = request.getfixturevalue(data_for_input)  # Словарь для записи в БД
    expected_data_from_db = request.getfixturevalue(data_from_db)  # Ожидаемые данные из БД

    protocol_manager.add_protocol_to_db(data_for_db)  # Записать данные в БД
    protocol = test_session.query(Protocol).first()
    keys_for_data_from_db = expected_data_from_db.keys()  # список всех атрибутов протокола

    assert protocol is not None
    assert protocol.number == expected_data_from_db['Номер протокола']
    assert protocol.date == expected_data_from_db['Дата протокола']

    # Проверяем, что каждый атрибут объекта protocol соответствует ожидаемому
    for attr in keys_for_data_from_db:
        if hasattr(protocol, KEYS_FOR_MAPPING_MODEL_PROTOCOL[attr]):
            received_value_of_field_from_db = getattr(
                protocol, KEYS_FOR_MAPPING_MODEL_PROTOCOL[attr])
            expected_value_of_field_from_db = expected_data_from_db[attr]

            assert received_value_of_field_from_db == expected_value_of_field_from_db


def test_delete_all_protocols_from_table(protocol_manager, test_session,
                                         data_from_word_file_1):
    """ Тест удаления всех протоколов из базы данных. """
    protocol_manager.add_protocol_to_db(data_from_word_file_1)
    protocol_manager.delete_all_protocols_from_table()
    protocols = test_session.query(Protocol).all()
    assert len(protocols) == 0
