"""
Модуль содержит функцию запуска всего кода пакета data_preparation

Пример использования:
    prepared_data_from_file = extract_and_prepare_data(path_to_word_file)

"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from league_sert.data_preparation.add_conclusions import add_conclusions_for_all_tables
from league_sert.data_preparation.file_parser import MainCollector
from league_sert.data_preparation.merge_tables import refine_and_merge_tables


def extract_and_prepare_data(word_file: str):
    """Запуск кода модуля."""
    data_collector = MainCollector(word_file)
    data_collector.collect_all_data()
    data_collector.data_from_tables = add_conclusions_for_all_tables(
        data_collector.data_from_tables
    )
    data_collector.data_from_tables = refine_and_merge_tables(data_collector.data_from_tables)
    data_collector.merge_prod_control()
    return data_collector
