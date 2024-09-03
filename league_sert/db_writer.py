""" Модуль с верхне-уровневым кодом записи данных в БД.

- Функции:
    - write_objects_to_db: записать переданный словарь объектов классов в БД.

    - process_and_write_files_to_db: получить путь к директории, через цикл
    обработать файлы и записать их в БД.

"""
import sys
import os

from pathlib import Path
from sqlalchemy.exc import IntegrityError

from database.db_config import prot_session_maker
from league_sert.data_preparation.launch_data_preparation import extract_and_prepare_data
from league_sert.models_creator import ObjectsForDB, create_objects


BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def write_objects_to_db(objects: ObjectsForDB):
    """ Записать объекты, сформированные из word файла в БД.
    :param: objects: объекты моделей, подлежащих записи в БД."""
    with prot_session_maker() as session:
        # try:
            for key, value in objects.items():
                # Добавление основного объекта в сессию
                if key[1] == 'MAIN':
                    main_object = value
                    session.add(value)
                # Добавление остальных объектов(привязанных через внешний ключ к основному).
                else:
                    for obj in value:
                        obj.main_prot = main_object
                        session.add(obj)
            session.commit()

        # except Exception as e:
        #     print(e)


def process_and_write_files_to_db(dir_path):
    """ Обработать и записать в БД все файлы,
    находящиеся в передаваемой директории """
    for i in os.listdir(dir_path):
        if '$' in i:
            continue
        data_from_file = extract_and_prepare_data(dir_path + '\\' + i)
        objects_for_db = create_objects(data_from_file)
        write_objects_to_db(objects_for_db)


if __name__ == '__main__':
    process_and_write_files_to_db(
        r'C:\Users\RIMinullin\Documents\протоколы'
        r'\почти полное от обыденникова\ППК для оцифровки'
        r'\Оригиналы_наилучшее возможное качество\word_files')
