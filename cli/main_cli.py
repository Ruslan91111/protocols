from cli.cli_db_manager import cli_db_manager
from cli.utils import divider, get_dir_from_user
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
            'Введите 1 и нажмите <Enter> для выполнения всего процесса.\n'
            
            'Введите 2 и нажмите <Enter> для конвертации файлов формата .pdf в формат .docx\n'
            
            'Введите 3 и нажмите <Enter> для записи всех файлов в Базу Данных.'
            'Обратите внимание, что файлы должны быть уже конвертированы\n'
            
            
            'Введите 4 и нажмите <Enter> для записи проблемных файлов с помощью корректировки '
            '.docx файлов.\n'
            
            'Введите 5 и нажмите <Enter> для переименования файлов в директории.\n'
            'Введите 6 и нажмите <Enter> для удаления страниц из файла формата .pdf.\n'
            'Введите 7 и нажмите <Enter> для работы с таблицами в БД.\n'
            'Введите 0 и нажмите <Enter> если хотите выйти.\n'
            '>>>'
        ))

        if choice_of_user == 2:
            path_from_user = get_dir_from_user()
            convert_all_pdf_in_dir_to_docx(path_from_user)

        if choice_of_user == 3:
            path_from_user = get_dir_from_user()
            write_files_to_db_from_dir(path_from_user)

        if choice_of_user == 4:
            path_from_user = get_dir_from_user()
            write_files_to_db_from_dir_debug(path_from_user)


        if choice_of_user == 5:
            path_from_user = get_dir_from_user()
            rename_the_files_in_dir(path_from_user)

        if choice_of_user == 6:
            path_from_user = get_dir_from_user()
            pages = input('Введите номера страниц, которые нужно удалить из ПДФ файла, '
                          'подряд без пробелов и других знаков, затем нажмите <Enter>,\n'
                          'либо введите слово <отмена> и нажмите <Enter>, если хотите выйти\n'
                          '>>>')
            pages = [int(i) for i in pages if i.isdigit()]
            remove_pdf_pages(path_from_user, pages)

        elif choice_of_user == 7:
            cli_db_manager()


if __name__ == '__main__':
    main_cli()
