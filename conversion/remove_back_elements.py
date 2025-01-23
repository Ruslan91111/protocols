"""
Модуль для удаления заднего фона из PDF файла

Этот модуль предоставляет инструменты для удаления фоновых изображений
и элементов (таких как синие фоновые изображения, оттиски печатей и рамки)
из PDF документов, в частности, из протоколов ФБУ.

Функционал модуля включает:
    - Улучшение контрастности изображений.
    - Перевод изображений в черно-белый формат.
    - Усиление черного и серого цветовых оттенков.
    - Обработка PDF файлов для удаления нежелательных фоновых элементов.

Функции:
    - improve_contrast(img): Улучшает контрастность изображения.
    - binarize_image(img): Переводит изображение в черно-белый формат.
    - enhance_black(img): Усиливает черный и серый цвет на изображении.
    - process_pdf(input_pdf_path, output_pdf_path): Обрабатывает PDF файл, применяя
      вышеуказанные методы к каждому изображению внутри документа.
    - rm_back_from_pdf_in_dir(dir_with_pdf_files: str) -> None: Удаляет фоновые элементы
      синего цвета из всех PDF файлов в указанной директории.


Примеры использования:
    - convert_pdf_to_word(DIR_ORIGINAL_PATH)

"""
import os
from PIL import Image
import fitz
import cv2
import numpy as np


POPPLER_PATH = r'/poppler-23.11.0/Library/bin'
os.environ['PATH'] += os.pathsep + POPPLER_PATH


def improve_contrast(img):
    """ Улучшить контрастность"""
    return cv2.convertScaleAbs(img, alpha=1.5, beta=0)


def binarize_image(img):
    """ Перевести изображение в черно - белый формат. """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)


def enhance_black(img):
    """Усилить черный и серый цвет на изображении."""
    # Преобразовать изображение в цветовое пространство HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Определить нижние и верхние границы черного и серого цветового диапазона
    l_black = np.array([0, 0, 0])  # Нижняя граница черного
    u_black = np.array([180, 255, 30])  # Верхняя граница черного

    l_gray = np.array([0, 0, 50])  # Нижняя граница серого
    u_gray = np.array([180, 18, 220])  # Верхняя граница серого

    # Создание масок для черного и серого цветов
    mask_black = cv2.inRange(hsv, l_black, u_black)
    mask_gray = cv2.inRange(hsv, l_gray, u_gray)

    # Применение черного цвета к найденным областям
    img[mask_black != 0] = [0, 0, 0]  # Применение черного к черным областям

    # Увеличиваем интенсивность для серых областей
    img[mask_gray != 0] = [50, 50, 50]  # Делаем серые области более темными

    return img


def rm_stamps_from_pdf(input_pdf_path, output_pdf_path):
    """ Обработать ПДФ файл, основное убрать из PDF файла оттиски печатей,
    подписи и другие изображения синего цвета. """

    # Открыть PDF
    doc = fitz.open(input_pdf_path)

    # Временная папка для изображений
    temp_dir = "temp_pages"
    os.makedirs(temp_dir, exist_ok=True)

    # Процесс извлечения страниц
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)

        # Извлечение изображения страницы
        pix = page.get_pixmap(dpi=300)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

        # Преобразование в BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Улучшение контрастности
        img = improve_contrast(img)

        # Удаление синих оттенков
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        img[mask != 0] = [255, 255, 255]

        # Бинаризация изображения
        img = binarize_image(img)
        img = enhance_black(img)

        # Сворачивание изображения в PDF
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        output_img_path = os.path.join(temp_dir, f"temp_page_{page_number}.png")
        img_pil.save(output_img_path, format='PNG', dpi=(450, 450))

        page.insert_image(page.rect, filename=output_img_path)

    # Сохранение обработанного PDF
    doc.save(output_pdf_path)

    # Удаление временных изображений
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)


def rm_back_from_pdf_in_dir(dir_with_pdf_files: str) -> None:
    """ Получить от пользователя путь к директории с PDF файлами
    через цикл обработать каждый файл и удалить с фона элементы синего
    цвета.

    - :param dir_original_pdf - директория с ПДФ файлами,
        нуждающимися в удалении фоновых изображений синего цвета. """

    for file in os.listdir(dir_with_pdf_files):
        rm_stamps_from_pdf(dir_with_pdf_files + '\\' + file, dir_with_pdf_files + '\\без фона ' + file)
