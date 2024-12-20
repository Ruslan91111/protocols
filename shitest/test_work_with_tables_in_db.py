# from pytest_lazyfixture import lazy_fixture
import copy
import pandas as pd
import pytest

from work_with_tables_in_db import KEYS_FOR_MAPPING_MODEL_PROTOCOL


def test_add_valid_store_to_db(store_manager, test_session):
    """ Тест добавления магазина в базу данных. """
    store_manager.add_store_to_db(1, 'Тестовый адрес')
    stores = store_manager.get_all_stores()[0]
    assert stores is not None
    assert stores.id == 1
    assert stores.address == 'Тестовый адрес'


def test_add_non_valid_store_to_db(store_manager, test_session):
    """ Тест добавления магазина в базу данных. """
    store_manager.add_store_to_db('неверный id', 'Тестовый адрес')
    stores = store_manager.get_all_stores()
    assert stores == []

    
def test_add_store_to_db_already_exists(store_manager, test_session):
    """ Тест добавления магазина в БД, когда магазин с таким id уже существует. """
    # Создаем магазин, добавляем в БД.
    store_manager.add_store_to_db(1, 'Тестовый адрес')
    # Пытаемся добавить магазин с таким же id.
    store_manager.add_store_to_db(1, 'Новый тестовый адрес')
    stores = store_manager.get_all_stores()
    assert stores is not None
    assert len(stores) == 1
    assert stores[0].id == 1
    assert stores[0].address == 'Тестовый адрес'


def test_fill_the_stores_from_file(store_manager, test_session):
    """ Тест заполнения таблицы stores из файла. """
    df = pd.DataFrame({'№ Магазина': [1, 2, 3], 'Адрес': ['Адрес 1', 'Адрес 2', 'Адрес 3']})
    path_excel = './test_stores.xlsx'
    df.to_excel(path_excel, index=False)
    store_manager.fill_the_stores_from_file(path_excel)
    stores = store_manager.get_all_stores()

    assert len(stores) == 3
    assert stores[0].id == 1
    assert stores[1].id == 2
    assert stores[2].id == 3
    assert stores[0].address == 'Адрес 1'
    assert stores[1].address == 'Адрес 2'
    assert stores[2].address == 'Адрес 3'


def test_delete_all_stores_from_table(store_manager, test_session):
    """ Тест удаления всех магазинов из базы данных. """
    store_manager.add_store_to_db(1, 'Адрес')
    store_manager.add_store_to_db(2, 'Другой адрес')
    store_manager.delete_all_stores_from_table()
    stores = store_manager.get_all_stores()
    assert len(stores) == 0


@pytest.mark.parametrize("data_for_input, data_from_db",
                         [("data_from_word_file_1", "data_from_db_1"),
                          ("data_from_word_file_2", "data_from_db_2"),
                          ("data_from_word_file_3", "data_from_db_3")])
def test_add_protocol_to_db(request, protocol_manager, test_session, data_for_input, data_from_db):
    """ Тест добавления протокола в базу данных. """
    data_for_db = request.getfixturevalue(data_for_input)  # Словарь для записи в БД
    expected_data_from_db = request.getfixturevalue(data_from_db)  # Ожидаемые данные из БД

    protocol_manager.create_protocol(data_for_db)  # Записать данные в БД
    protocol = protocol_manager.get_all_protocols()[0]
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


def test_add_protocol_to_db_already_exist(protocol_manager,
                                      data_from_word_file_1):
    """ Тест добавления протокола в базу данных. """
    data_for_first_object = data_from_word_file_1  # Словарь для записи в БД
    protocol_manager.create_protocol(data_for_first_object)  # Записать данные в БД
    data_for_object_with_same_id = copy.deepcopy(data_for_first_object)
    data_for_object_with_same_id['Сопроводительные документы'] = 1
    protocol_manager.create_protocol(data_for_object_with_same_id)  # Записать данные в БД
    protocols = protocol_manager.get_all_protocols()
    assert len(protocols) == 1  # Проверка, что в БД один объект и второй не записан
    protocol = protocols[0]
    # Проверка, что данные, внесенные первой записью не изменились
    assert protocol.accompanying_documents == data_for_first_object['Сопроводительные документы']


def test_delete_all_protocols_from_table(protocol_manager, test_session,
                                         data_from_word_file_1, data_from_word_file_2):
    """ Тест удаления всех протоколов из базы данных. """
    protocol_manager.create_protocol(data_from_word_file_1)
    protocol_manager.create_protocol(data_from_word_file_2)
    protocols = protocol_manager.get_all_protocols()
    assert len(protocols) == 2
    protocol_manager.delete_all_protocols_from_table()
    protocols = protocol_manager.get_all_protocols()
    assert len(protocols) == 0
