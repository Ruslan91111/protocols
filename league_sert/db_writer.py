""" Модуль с верхне-уровневым кодом записи данных в БД.

- Функции:
    - write_objects_to_db: записать переданный словарь объектов классов в БД.

    - process_and_write_files_to_db: получить путь к директории, через цикл
    обработать файлы и записать их в БД.

"""
import re
import sys
import os
import time

from pathlib import Path

from database.db_config_postgres import prot_session_maker
from league_sert.data_preparation.launch_data_preparation import extract_and_prepare_data
from league_sert.models.models_creator import ObjectsForDB, create_all_objects


BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


VIEWED_FILE = r'viewed.txt'


def write_objects_to_db(objects: ObjectsForDB, session_maker):
    """ Записать объекты, сформированные из одного word файла в БД.

    Сначала в БД записывается основной объект, затем он передается
    в дополнительные объекты для оформления внешних связей.

    :param: objects: объекты моделей, подлежащих записи в БД."""

    with session_maker() as session:
        try:
            for key, value in objects.items():
                # Добавление основного объекта (с основным номером и датой протокола) в сессию.
                if key[1] == 'MAIN':
                    main_object = value
                    session.add(value)

            # Перебираем объекты собранные и подготовленные для записи в БД.
            for key, value in objects.items():
                # Добавление остальных объектов в сессию.
                if key[1] != 'MAIN':
                    for obj in value:
                        # Добавляем ссылку на основной объект.
                        obj.main_prot = main_object
                        session.add(obj)
            session.commit()

        except Exception as e:
            print(e)


def write_file_to_db(file):
    """ Записать один word файл в БД."""
    # Собрать данные из word файла.
    data_from_file = extract_and_prepare_data(file)
    # Создать из собранных данных объекты для записи в БД.
    objects_for_db = create_all_objects(data_from_file)
    # Записать объекты в БД.
    write_objects_to_db(objects_for_db, prot_session_maker)


def read_viewed_from_file(file: str = VIEWED_FILE):
    """Прочитать номера просмотренных документов из файла."""

    if not os.path.isfile(file):
        with open(file, 'w', encoding='utf-8') as file:
            file.write('')
            return set()

    with open(file, 'r', encoding='utf-8') as file:
        viewed_files = set(file.read().split(','))
        return viewed_files


def write_files_to_db_from_dir(dir_path):
    """ Обработать и записать в БД все файлы,
    находящиеся в передаваемой директории """

    not_recorded = []  # Файлы, незаписанные в БД.

    recorded =read_viewed_from_file(VIEWED_FILE)
    for file in os.listdir(dir_path):
        if '$' in file or file in recorded:
            continue

        try:
            print(file)
            # Получить и подготовить данные из word файла
            data_from_file = extract_and_prepare_data(dir_path + '\\' + file)
            # Создать объекты для записи в БД.
            objects_for_db = create_all_objects(data_from_file)
            # Записать объекты в БД.
            write_objects_to_db(objects_for_db, prot_session_maker)
            # Добавить в записанный
            recorded.add(file)

        except Exception as e:
            not_recorded.append(file)
            with open(VIEWED_FILE, 'w', encoding='utf-8') as file:
                file.write(",".join(recorded))

    with open(VIEWED_FILE, 'w', encoding='utf-8') as file:
        file.write(",".join(recorded))

    print(f'pas {len(recorded)}')
    print(f'unpas {len(not_recorded)}')
