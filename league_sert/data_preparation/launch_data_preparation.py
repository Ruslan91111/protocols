"""

Модуль содержит функцию запуска всего кода пакета data_preparation

Пример использования:
    prepared_data_from_file = extract_and_prepare_data(path_to_word_file)

"""
import os
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
    data_getter = MainCollector(word_file)
    data_getter.collect_all_data()
    data_getter.data_from_tables = add_conclusions_for_all_tables(data_getter.data_from_tables)
    return refine_and_merge_tables(data_getter.data_from_tables)


path = r'C:\Users\RIMinullin\Documents\протоколы\почти полное от обыденникова\ППК для оцифровки\Оригиналы_наилучшее возможное качество\word_files'
for i in os.listdir(path):
    print(i)
    if '$' in i:
        continue
    print(extract_and_prepare_data(path+'\\' +i))
lst = ['44433 29.05.2024.docx',
       '47109 23.05.2024.docx',
       '47116 23.05.2024.docx',
       '47120 24.05.2024.docx',

       '47190 08.04.2024.docx',
       '50445 03.05.2024.docx',
       '77367 12.04.2024.docx',]

# print(extract_and_prepare_data(path + '\\' + lst[-1]))