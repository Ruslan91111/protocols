import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if BASE_DIR not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from compress_pdfs.compress_file_aspose_pdf import compress_files_in_dir
from cli_db_manager import cli_db_manager
from utils import divider, get_dir_from_user
from conversion.convert_files_all import convert_all_pdf_in_dir_to_docx
from conversion.remove_pages_in_pdf import remove_pdf_pages
from league_sert.db_operations.db_writer import write_files_to_db_from_dir
from league_sert.manual_entry.db_writer_debug import write_files_to_db_from_dir_debug
from rename_files.rename_files import rename_the_files_in_dir


def main_cli():
    choice_of_user = True
    divider()
    print('Общее меню')
    while True and choice_of_user != 0:
        divider()
        choice_of_user = int(input(
            'Введите 1 и нажмите <Enter> для выполнения всего процесса от конвертации файлов'
            'до записи в Базу Данных.\n'
            
            'Введите 2 и нажмите <Enter> для конвертации файлов формата .pdf в формат .docx\n'           
            
            'Введите 3 и нажмите <Enter> для записи всех файлов в Базу Данных.'
            'Обратите внимание, что речь идет только о записи данных в Базу Данных,'
            ' файлы должны быть уже конвертированы\n'
        
            'Введите 4 и нажмите <Enter> для записи проблемных файлов с помощью корректировки '
            '.docx файлов.\n'
            
            'Введите 5 и нажмите <Enter> для переименования файлов в директории по принципу '
            'код магазина, дата протокола.\n'
            
            'Введите 6 и нажмите <Enter> для сжатия файлов в директории.\n'
            
            'Введите 7 и нажмите <Enter> для удаления страниц из файла формата .pdf.\n'
            
            'Введите 8 и нажмите <Enter> для перехода в меню работы с таблицами в БД.\n'
            
            'Введите 0 и нажмите <Enter> если хотите выйти.\n'
            '>>>'
        ))

        # Весь процесс от конвертации до записи в БД через корректировки.
        if choice_of_user == 1:
            path_from_user = get_dir_from_user()
            convert_all_pdf_in_dir_to_docx(path_from_user)
            rename_the_files_in_dir(path_from_user)
            compress_files_in_dir(path_from_user)
            write_files_to_db_from_dir(path_from_user)
            # write_files_to_db_from_dir_debug(path_from_user)

        # Конвертация всех файлов ПДФ в директории.
        if choice_of_user == 2:
            path_from_user = get_dir_from_user()
            convert_all_pdf_in_dir_to_docx(path_from_user)
            print('Файлы в директории конвертированы.')

        # Запись всех файлов в БД.
        if choice_of_user == 3:
            path_from_user = get_dir_from_user()
            write_files_to_db_from_dir(path_from_user)
            print('Данные из файлов записаны в Базу Данных.')

        # Запись файлов через корректировки word файлов.
        if choice_of_user == 4:
            path_from_user = get_dir_from_user()
            write_files_to_db_from_dir_debug(path_from_user)
            print('Запись данных в Базу Данных через корректировки word файлов окончена.')

        # Переименовать файлы в директории.
        if choice_of_user == 5:
            path_from_user = get_dir_from_user()
            rename_the_files_in_dir(path_from_user)
            print('Файлы в директории переименованы.')

        # Сжать файлы ПДФ в директории.
        if choice_of_user == 6:
            path_from_user = get_dir_from_user()
            compress_files_in_dir(path_from_user)
            print('Файлы формата .pdf в директории сжаты.')

        # Удалить страницы из ПДФ файла
        if choice_of_user == 7:
            path_from_user = get_dir_from_user()
            pages = input('Введите номера страниц, которые нужно удалить из ПДФ файла, '
                          'подряд без пробелов и других знаков, затем нажмите <Enter>,\n'
                          'либо введите слово <отмена> и нажмите <Enter>, если хотите выйти\n'
                          '>>>')
            pages = [int(i) for i in pages if i.isdigit()]
            remove_pdf_pages(path_from_user, pages)
            print('Страницы удалены из файла формата .pdf')

        # Работа с таблицами в БД.
        elif choice_of_user == 8:
            print('Вы перешли в меню работы с таблицами в Базе Данных.')
            cli_db_manager()


if __name__ == '__main__':
    main_cli()
