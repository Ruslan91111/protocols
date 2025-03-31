"""
Пример сжатия файла с использованием библиотеки aspose.
Сжимает, сохраняет качество, оставляет водный знак, красная строка на странице,
нужна лицензия
"""
import os
from pathlib import Path

import aspose.pdf as ap


def compress_file_with_aspose(input_pdf: str | Path,
                              output_pdf: str | Path,
                              image_quality: int = 50,
                              dpi: int = 120):
    """
    Сжать pdf файл.

    :param input_pdf:
    :param output_pdf:
    :param image_quality: Качество изображения от 0 до 100.
    :param dpi:
    :return: None
    """

    # Проверка переданных аргументов.
    if not os.path.isfile(input_pdf):
        raise FileNotFoundError(f"Файл '{input_pdf}' не найден.")
    if not (0 < image_quality <= 100) or not isinstance(image_quality, int):
        raise ValueError("image_quality должно быть целое число в диапазоне от 0 до 100.")
    if not (72 <= dpi <= 600) or not isinstance(dpi, int):
        raise ValueError("dpi должно быть целое число в диапазоне от 72 до 600.")

    # Загрузить PDF-файл.
    input_pdf = ap.Document(input_pdf)

    # Создать объект класса OptimizationOptions.
    pdf_optimize_options = ap.optimization.OptimizationOptions()

    # Включить сжатие изображений.
    pdf_optimize_options.image_compression_options.compress_images = True

    # Установить качество изображения.
    pdf_optimize_options.image_compression_options.image_quality = image_quality

    # Установить максимальное разрешение изображений.
    pdf_optimize_options.image_compression_options.max_resolution = dpi

    # Включить изменение размера изображений
    pdf_optimize_options.image_compression_options.resize_images = True

    # Сжать PDF
    input_pdf.optimize_resources(pdf_optimize_options)

    # Сохранить сжатый PDF
    input_pdf.save(output_pdf)
