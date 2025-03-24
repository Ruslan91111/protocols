"""
Код, отвечающий за запись данных из html файлов в БД.
"""
import multiprocessing
import os
from pathlib import Path
from sqlite3 import IntegrityError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.db_config_postgres import PROTOCOLS_DB
from league_sert.db_writer_proc import read_viewed_from_file
from league_sert.exceptions import DirDontExistError
from quarantine_acts.models import QuarantineAct
from quarantine_acts.parse_file import create_instance_of_model_from_html

VIEWED_FILE_QUARANTINE_ACTS = 'viewed_quarantine_acts.txt'


def _add_instance_to_db(instance: QuarantineAct, session_maker):
    """Записать объект, сформированные из одного word файла в БД."""

    with session_maker() as session:

        try:
            # Проверяем нет ли уже в БД акта с таким же номером. Если нет, то записываем в БД.
            existing_main = session.query(QuarantineAct).filter_by(number=instance.number).first()
            if not existing_main:
                session.add(instance)
            else:
                print(f'Объект с номером {existing_main.number} уже существует в БД.')
            session.commit()

        # Отлавливаем исключение, если аналогичный номер уже есть в БД.
        except IntegrityError as e:
            session.rollback()
            print('УЖЕ ЕСТЬ В БД.', e)
            # Поднимаем исключение, чтобы отловить в основном процессе.
            raise

        # Отлавливаем иное исключение.
        except Exception as e:
            session.rollback()
            print(f"Произошла ошибка при записи в БД: {e}")
            raise


def process_file(file, dir_path, recorded, db_url):
    """Обработать один html файл."""
    engine = create_engine(db_url, echo=True)
    session = sessionmaker(bind=engine)

    # Пропускаем временный файл, уже записанный в БД файл, директории
    if '$' in file or file in recorded or os.path.isdir(os.path.join(dir_path, file)):
        return None, file  # Пропустить файл

    try:
        file_full_path = os.path.join(dir_path, file)  # Полный путь к файлу.
        model_instance = create_instance_of_model_from_html(Path(file_full_path))  # Объект модели.
        _add_instance_to_db(model_instance, session)  # Добавление объекта в БД.
        return file, None  # Успешно обработан и записан в БД.

    except Exception as e:
        print(f"Ошибка обработки файла {file}: {e}")

    return None, file


def write_files_to_db_from_dir(dir_path, db_url, num_processes=4):
    """Обработать и записать в БД данные из всех файлов, находящиеся в передаваемой директории,
    используя многопроцессорность."""

    # Если директории не существует.
    if not os.path.isdir(dir_path):
        raise DirDontExistError(dir_path)

    # Проверяем и при необходимости создаем
    html_dir = os.path.join(dir_path, 'html_files')
    if not os.path.isdir(html_dir):
        os.mkdir(html_dir)

    not_recorded = []  # Файлы, незаписанные в БД.
    recorded = read_viewed_from_file(VIEWED_FILE_QUARANTINE_ACTS)  # Файлы, уже записанные в БД.

    # Собираем айлы для обработки, опускаем временные файлы, ранее проверенные
    # и директории.
    files_to_process = [
        os.path.join(html_dir, f) for f in os.listdir(html_dir)
        if not ('$' in f or f in recorded or os.path.isdir(os.path.join(html_dir, f)))
    ]

    # Создаем пул процессов для изъятия данных из файлов и записи в БД.
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(
            process_file, [(file, dir_path, recorded, db_url) for file in files_to_process]
        )

    # Распределяем обработанные и необработанные файлы в соответствующие списки.
    for recorded_file, not_recorded_file in results:
        if recorded_file:
            recorded.add(recorded_file.split("\\")[-1])
        if not_recorded_file:
            not_recorded.append(not_recorded_file)

    # Обновить файл с записанными файлами.
    with open(VIEWED_FILE_QUARANTINE_ACTS, 'w', encoding='utf-8') as word_file:
        word_file.write(",".join(recorded))

    print(f'В Базу Данных записано {len(recorded)} файлов.')


if __name__ == '__main__':
    directory = r'C:\Users\RIMinullin\Desktop\что-то новое'
    write_files_to_db_from_dir(directory, PROTOCOLS_DB)
