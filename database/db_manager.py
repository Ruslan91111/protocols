"""
Модуль с классом для выполнения общих манипуляций с БД.

Класс:

    DBManager:
        - Класс для общих манипуляций с БД и таблицами в ней.

        - Методы:
            - create_all_tables
            - drop_all_tables
            - get_all_tables
            - drop_the_table
            - get_table_contents

    Пример использования:
        if __name__ == '__main__':
            db_manager = DBManager(Base, protocols_engine)
            db_manager.method()

"""
import sys
from pathlib import Path
from sqlalchemy import MetaData, Table, select

BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.db_config_postgres import protocols_engine, prot_session_maker
from database.base import Base

from league_sert.models.models import *
from fbu_protocols.models.models import *


class DBManager:
    """ Класс для общих манипуляций с БД и таблицами в ней. """
    def __init__(self, base, engine, session):
        self.Base = base
        self.metadata = MetaData()
        self.engine = engine
        self.session = session

    def create_all_tables(self):
        """Создать все таблицы, определенные в модели Base."""
        self.Base.metadata.create_all(bind=self.engine)
        print("Все таблицы созданы")

    def drop_all_tables(self):
        """Удалить все таблицы, определенные в модели Base."""
        self.Base.metadata.drop_all(bind=self.engine)
        print("Все таблицы удалены")

    def get_session(self):
        """Получить сессию базы данных."""
        return self.session()

    def get_all_tables(self):
        """Вернуть все таблицы и поля, находящиеся в БД."""
        self.metadata.reflect(bind=self.engine)
        return self.metadata.tables

    def drop_the_table(self, table_name):
        """Удалить таблицу из БД."""
        self.metadata.reflect(bind=self.engine)
        # Проверяем, существует ли таблица
        if table_name in self.metadata.tables:
            table = Table(table_name, self.metadata, autoload=True, autoload_with=self.engine)
            table.drop(self.engine)
            print(f"Таблица '{table_name}' успешно удалена.")
        else:
            print(f"Таблица '{table_name}' не найдена в базе данных.")

    def get_table_contents(self, table_name):
        """Получить содержимое таблицы по названию."""
        with self.get_session() as session:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            stmt = select(table)
            result = session.execute(stmt)
            rows = result.fetchall()

            if rows:
                print(f'Содержимое таблицы {table_name}:')
                for row in rows:
                    print(row)
            else:
                print(f"Таблица '{table_name}' пуста или не существует.")


if __name__ == '__main__':
    db_worker = DBManager(Base, protocols_engine, prot_session_maker)
    db_worker.drop_all_tables()
    db_worker.create_all_tables()
