""" Фикстуры, используемые более, чем в одном модуле. """
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from tests.test_league_sert.data_for_main_collector import data_for_main_collector


class MainCollectorDoubler:
    """ Дублер класса MainCollector. """

    def __init__(self, attrs_dict):
        for key, value in attrs_dict.items():
            setattr(self, key, value)


@pytest.fixture(scope='module')
def main_collector():
    """ Создание объекта - дублера класса MainCollector. """
    return MainCollectorDoubler(data_for_main_collector)


@pytest.fixture()
def create_test_engine():
    """ Создать тестовый движок. """
    TEST_DB = f'sqlite:///:memory:'
    test_engine = create_engine(TEST_DB)
    return test_engine


@pytest.fixture()
def create_test_session(create_test_engine):
    """ СОздать тестовую сессию """
    session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=create_test_engine
    )
    return session_maker


@pytest.fixture(autouse=True)
def setup_and_teardown(create_test_engine):
    """ Фикстура для создания и удаления таблиц перед и после каждого теста. """
    Base.metadata.create_all(bind=create_test_engine)  # Создать таблицы в БД.
    yield
    Base.metadata.drop_all(bind=create_test_engine)  # Удалить таблицы после теста.
