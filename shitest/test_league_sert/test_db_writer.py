import datetime

from sqlalchemy import text

from league_sert.db_writer import write_objects_to_db

from league_sert.models.models_creator import create_all_objects
from tests.test_league_sert.conftest import (main_collector,
                                             create_test_engine,
                                             create_test_session)


def test_write_objects_to_db(main_collector, create_test_engine, create_test_session):
    """ Протестировать создание объектов в БД в рамках одной сессии. """
    # Base.metadata.create_all(bind=create_test_engine)  # Создать таблицы в БД.
    objects_to_write_in_db = create_all_objects(main_collector)
    write_objects_to_db(objects_to_write_in_db,
                        create_test_session)  # Запись в БД.

    with create_test_engine.connect() as connection:
        main_prot = connection.execute(text('select * from main_prot'))
        main_prot = main_prot.fetchall()

        assert len(main_prot) == 1

        assert main_prot[0].id == 1
        assert main_prot[0].number == '4225/24-Д'
        assert main_prot[0].date == '2024-05-23'
        assert main_prot[0].store_address == (
            'Ленинградская область, Гатчинский р-н, г. Гатчина, ул. Куприна, д. 48, л. А'
        )
        assert main_prot[0].store_code == 47109

        manuf_prod = connection.execute(text('select * from manuf_prod'))
        manuf_prod = manuf_prod.fetchall()
        assert len(manuf_prod) == 41
        assert manuf_prod[0].main_prot_id == 1

        prod_control = connection.execute(text('select * from prod_control'))
        prod_control = prod_control.fetchall()
        assert len(prod_control) == 6
        assert prod_control[0].main_prot_id == 1


