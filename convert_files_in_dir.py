"""
Модуль для конвертации файлов в папке из pdf в txt.

Файл содержит код, направленный на конвертацию файлов из формата pdf в формат txt.
для запуска вызвать функцию convert_all_pdf_in_dir_to_word(), затем ввести путь к папке
с файлами в формате txt. Конвертация будет осуществляться через программу FineReader
при помощи pyautogui. Код работает через цикл.

    def wait_and_click_on_the_screenshot() - кликнуть по скриншоту
    def wait_for_the_screenshot_to_disappear() - ждать исчезновение скриншота
    def find_screenshot_in_screenshot() - найти скриншот в скриншоте и кликнуть по нему
    def change_keyboard_layout_on_english(): - переключить раскладку в системе на английскую
    def hide_the_windows() - свернуть все окна
    def return_or_create_dir() - проверить наличие папки, если нет, то создать
    def launch_desktop_app() - запустить приложение FineReader
    def terminate_the_proc() - прекратить процесс в windows
    def get_from_user_path_for_existing_dir() - получить от пользователя путь к папке
    def get_files_required_to_convert() - Вернуть множеством файлы, которые нужно конвертировать.
    def input_filename() - Ввести название файла в поле приложения.
    def convert_all_pdf_in_dir_to_word() - основная функция по преобразованию файлов из
        формата word в формат pdf

    Пример использования:
        convert_all_pdf_in_dir_to_word()

"""
import os.path
import time
from enum import Enum
from typing import Optional
import psutil
import py_win_keyboard_layout
import pyautogui
import pyperclip

from exceptions import ScreenshotNotFoundException


##################################################################################
# Константы и enum классы
##################################################################################
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
    INPUT_FILE_NAME: str = r'../screenshots/input_file_name.png'
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


##################################################################################
# Функции работы со скриншотами.
##################################################################################
def wait_and_click_on_the_screenshot(screenshot_path: str,
                                     timeout: int = 30,
                                     confidence: float = 0.8) -> tuple[float] | None:
    """ Ожидать появление скриншота в течение заданного времени.
     При обнаружении кликнуть по нему один раз. """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            time.sleep(0.03)
            image = pyautogui.locateOnScreen(screenshot_path, confidence=confidence)
            # Если скриншот найден кликнуть по нему и вернуть его координаты
            if image:
                pyautogui.click(image)
                return image
        except pyautogui.ImageNotFoundException:
            pass
    # Поднять исключение, если скриншот не найден в течении заданного периода времени.
    raise ScreenshotNotFoundException(screenshot_path)


def wait_for_the_screenshot_to_disappear(screenshot: str,
                                         timeout: int = 10,
                                         confidence: float = 0.8) -> Optional[False]:
    """ Ждем пока определенный скриншот не исчезнет с экрана.

    В течении заданного периода времени ищем скриншот на экране. Если находим,
    то продолжаем искать, если не находим, то выходим из функции и возвращаем None.
    Если в течении заданного времени скриншот с экрана не ушел, то возвращаем False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            time.sleep(0.05)
            # Ищем скриншот.
            image = pyautogui.locateOnScreen(screenshot, confidence=confidence)
            # Если найден, то продолжаем его находить.
            if image:
                pass
        except pyautogui.ImageNotFoundException:
            return None
    return False


def find_screenshot_in_screenshot(inner_image_path: str,
                                  external_image_path: tuple [float] | None,
                                  confidence: float = 0.7):
    """ Найти скриншот в скриншоте и кликнуть по внутреннему скриншоту. """
    found_inner_screenshot = pyautogui.locateOnScreen(
        inner_image_path, region=external_image_path, confidence=confidence)
    if found_inner_screenshot:
        pyautogui.click(found_inner_screenshot)


##################################################################################
# Функции, связанные с работой с процессами, папками и файлами.
##################################################################################
def change_keyboard_layout_on_english():
    """ Переключить раскладку клавиатуры на английскую. """
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)


def hide_the_windows():
    """ Свернуть все окна"""
    pyautogui.hotkey('Win', 'd')


def return_or_create_dir(path_to_dir: str):
    """ Вернуть или создать директорию. """
    if not os.path.isdir(path_to_dir):
        os.mkdir(path_to_dir)
        print("Создана директория <%s>." % path_to_dir)
    else:
        print("Проверено наличие директории <%s>. Директория существует. " % path_to_dir)
    return path_to_dir


def launch_desktop_app(process: str, icon_from_panel: str,
                       icon_from_desktop: str, confidence: float = 0.8) -> None:
    """ Проверяет запущен ли переданный процесс в ОС. Если процесс(окно) запущено, то
    раскрываем кликом по иконке на панели. Если нет, то кликаем по иконке на рабочем столе. +"""
    change_keyboard_layout_on_english()
    hide_the_windows()

    # Перебираем текущие процессы и ищем нужный нам процесс.
    for proc in psutil.process_iter():
        name = proc.name()
        # Если нужный процесс запущен.
        if name == process:
            # Кликнуть по иконке на нижней панели, чтобы развернуть окно.
            wait_and_click_on_the_screenshot(icon_from_panel, confidence=confidence)
            return None
    # Если нужный процесс не запущен, то запускаем по иконке с рабочего стола.
    wait_and_click_on_the_screenshot(icon_from_desktop, confidence=confidence)
    pyautogui.hotkey('enter')
    return None


def terminate_the_proc(process: str) -> None:
    """ Закрыть переданный процесс. """
    # Перебираем текущие процессы и ищем нужный нам процесс.
    for proc in psutil.process_iter():
        name = proc.name()
        # Если нужный процесс запущен.
        if name == process:
            proc.terminate()
            break


def get_from_user_path_for_existing_dir(message_for_user: str) -> str:
    """Получить путь от пользователя к существующей директории."""
    path_from_user = input(message_for_user)
    print(path_from_user)
    # Если путь указан неверно.
    if not path_from_user:
        raise Exception("Путь не введен")
    # Если файл не существует.
    if not os.path.isdir(path_from_user):
        raise Exception("Указанный путь не существует")
    return path_from_user


def get_files_required_to_convert(path_to_dir_pdf: str, path_to_dir_word: str) -> set:
    """Вернуть множеством файлы, которые нужно конвертировать."""
    pdf_files = {i for i in os.listdir(path_to_dir_pdf) if i[-4:] == '.pdf'}
    pdf_files = {i[:-4] for i in pdf_files}
    word_files = {i for i in os.listdir(path_to_dir_word) if i[-5:] == '.docx'}
    word_files = {i[:-5] for i in word_files}
    set_files_required_to_convert = pdf_files.difference(word_files)
    return set_files_required_to_convert


def input_filename(directory: str, file: str):
    """ Ввести название файла в поле приложения. """
    wait_and_click_on_the_screenshot(FineReaderScreenshots.INPUT_FILE_NAME.value)
    x, y = pyautogui.position()
    pyautogui.click(x + 80, y)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    filename_pdf = '\\' + directory + '\\' + file
    pyperclip.copy(filename_pdf.replace('\\\\', '\\'))
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')


##################################################################################
# Главная функция модуля.
##################################################################################
def convert_all_pdf_in_dir_to_word() -> None:
    """ Получить от пользователя путь к директории с PDF файлами и путь к директории,
    в которую будут сохранены файлы в формате word после конвертации. """
    # Получить от пользователя пути к: 1) директория с пдф файлами и 2) word файлами
    dir_with_pdf_files = get_from_user_path_for_existing_dir(
        MESSAGE_FOR_USER_GET_DIR_WITH_PDF_FILES)
    dir_for_word_files = return_or_create_dir(dir_with_pdf_files + '\\word_files\\')

    # Перечень файлов, которые еще не конвертированы.
    files_required_to_convert = get_files_required_to_convert(dir_with_pdf_files,
                                                              dir_for_word_files)
    # Запустить FineReader.
    launch_desktop_app(FINE_READER_PROCESS,
                       FineReaderScreenshots.FINE_READER_PANEL.value,
                       FineReaderScreenshots.FINE_READER_DESKTOP.value,
                       0.8)

    # Дождаться полной загрузки FineReader.
    wait_for_the_screenshot_to_disappear(FineReaderScreenshots.FINE_READER_LOADING.value)

    # Проверяем не находимся ли в подразделе "Конвертировать в Microsoft Word"
    try:
        wait_and_click_on_the_screenshot(FineReaderScreenshots.BUTTON_CANCEL.value, timeout=5)
    except ScreenshotNotFoundException:
        pass

    # Перебираем файлы в перечне файлов, нуждающихся в конвертации.
    for file in files_required_to_convert:

        # Главное меню, кликнуть по кнопке конвертировать.
        wait_and_click_on_the_screenshot(
            FineReaderScreenshots.BUTTON_CONVERT_TO_WORD_MAIN_MENU.value)

        # Ввести путь и наименование файла PDF, который нужно конвертировать.
        input_filename(dir_with_pdf_files, file)

        # Убрать галочку с сохранения рисунка
        outer_image = wait_and_click_on_the_screenshot(
            FineReaderScreenshots.REMOVE_MARK_FROM_SAVE_PICTURES.value)
        find_screenshot_in_screenshot(FineReaderScreenshots.REMARK.value,
                                      outer_image)

        # Нажать синюю кнопку конвертировать в Word.
        wait_and_click_on_the_screenshot(FineReaderScreenshots.BLUE_BUTTON_CONVERT_TO_WORD.value)

        # Ввести путь и наименование word файла, в котором будет сохранен результат конвертации.
        input_filename(dir_for_word_files, file)

        # Нажать кнопку сохранить.
        wait_and_click_on_the_screenshot(FineReaderScreenshots.SAVE_BUTTON.value)
        time.sleep(40)

        # Закрыть word файл, который открывается автоматически после конвертации.
        terminate_the_proc(WORD_PROCESS)

        # Нажать кнопку отмены в меню.
        wait_and_click_on_the_screenshot(FineReaderScreenshots.BUTTON_CANCEL.value)
        time.sleep(1)


if __name__ == '__main__':
    convert_all_pdf_in_dir_to_word()
