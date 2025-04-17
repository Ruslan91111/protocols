""" Исключения для пакета conversion. """


class ScreenshotNotFoundError(Exception):
    """Не найден скриншот - ошибка, которая делает невозможным
    дальнейшее выполнение программы."""
    def __init__(self, image_path):
        self.image_path = image_path
        super().__init__(f"Не найден скриншот - {image_path} ")


class PathNotInputError(Exception):
    """ Путь не введен. """
    def __init__(self):
        super().__init__("Путь не введен")


class InvalidPathError(Exception):
    """ Указанный путь не существует. """
    def __init__(self):
        super().__init__("Указанный путь не существует. ")


class DateNotFoundError(Exception):
    """ Указанный путь не существует. """
    def __init__(self, path_word_file):
        super().__init__(f"Не найдена дата протокола в файле {path_word_file}")


class StoreCodeError(Exception):
    """ Указанный путь не существует. """
    def __init__(self, path_word_file):
        super().__init__(f" В файле {path_word_file} не найден код магазина.")


class NumbDateNotFoundError(Exception):
    """ Указанный путь не существует. """
    def __init__(self, file):
        super().__init__(f"При конвертации файла <{file}> "
                         f"не найдены номер и дата протокола.")


class PageNeedToRMError(Exception):
    """ Указанный путь не существует. """
    def __init__(self, file):
        super().__init__(f"При конвертации файла <{file}> возникла ошибка, необходимо удалить "
                         f"одну из страниц. ")


class NoDirWithWordFilesError(Exception):
    """ Указанный путь не существует. """
    def __init__(self, path_dir):
        super().__init__(
            f"В переданной директории <{path_dir}> отсутствует директория "
            f"с конвертированными word файлами. Переименование невозможно.")
