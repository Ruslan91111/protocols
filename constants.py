from enum import Enum


DIR_WITH_PDF_FILES = r'C:\Users\RIMinullin\Desktop\для ворда\в высоком качестве'


class FineReaderScreenshots(Enum):
    """
    Пути к скриншотам, необходимым для работы с FineReader с помощью pyautogui.
    """
    FINE_READER_DESKTOP: str = r'./screenshots/fine_reader_desktop.png'
    FINE_READER_PANEL: str = r'./screenshots/fine_reader_panel.png'
    FINE_READER_LOADING: str = r'./screenshots/fine_reader_loading.png'
    BUTTON_CONVERT_TO_WORD_MAIN_MENU: str = r'./screenshots/button_convert_to_word_main_menu.png'
    BLUE_BUTTON_CONVERT_TO_WORD: str = r'./screenshots/blue_button_convert_to_word.png'
    DATA_OF_MODIFICATION: str = r'./screenshots/data_of_modification.png'
    INPUT_FILE_NAME: str = r'./screenshots/input_file_name.png'
    PROCESS_OF_CONVERSION: str = r'./screenshots/process_of_conversion.png'
    BUTTON_CANCEL: str = r'./screenshots/button_cancel.png'
    SAVE_BUTTON: str = r'./screenshots/save_button.png'
    REMOVE_MARK_FROM_SAVE_PICTURES: str = r'./screenshots/save_pictures.png'
    REMARK: str = r'./screenshots/remark.png'


FINE_READER_PROCESS = 'FineReader.exe'
WORD_PROCESS = 'WINWORD.EXE'
MESSAGE_FOR_USER_GET_DIR_WITH_PDF_FILES = (
    'Введите полный путь (включая сетевой диск) до директории, '
    'в которой находятся файлы формата PDF, нуждающиеся в конвертации в формат Word:'
    '\n>>>')
MESSAGE_FOR_USER_GET_DIR_WITH_WORD_FILES = (
    'Введите полный путь (включая сетевой диск) до директории, '
    'в которой будут находиться файлы Word после конвертации:'
    '\n>>>')

# Ключи для поиска на первой странице протокола.
REQUIRED_KEYS_FOR_PARSING_FIRST_PAGE = (
    'Место отбора проб',
    'Дата и время отбора проб',
    'Сопроводительные документы',
    'Группа продукции',
    'Наименование продукции',
    'Дата производства продукции',
    'Производитель (фирма, предприятие, организация)',
    'Дата проведения исследований'
)
