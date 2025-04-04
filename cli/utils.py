import os


def divider():
    """ Просто вывести разделитель в виде множества знаков = """
    print('==' * 80)


def get_dir_from_user():
    """ Получить от пользователя путь до директории. """

    while True:
        divider()
        path_from_user = input('Введите полный путь до директории с файлами, затем нажмите <Enter>\n'
                               '>>>').strip()

        if path_from_user == 0:
            return False
        elif not os.path.isdir(path_from_user):
            print('Введен неверный путь, попробуйте еще раз. Либо введите 0 и нажмите <Enter> для выхода.')
        else:
            return path_from_user


def get_file_from_user():
    """ Получить от пользователя путь до файла. """

    while True:
        divider()
        path_from_user = input('Введите полный путь до файла, затем нажмите <Enter>. '
                               'Либо введите 0 и нажмите <Enter> для выхода.\n'
                               '>>>').strip()

        if path_from_user == 0:
            return False
        elif not os.path.isfile(path_from_user):
            print('Введен неверный путь, попробуйте еще раз. Либо введите 0 и нажмите <Enter> для выхода.')
        else:
            return path_from_user
