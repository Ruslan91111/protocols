""" Уменьшить размер pdf файла. """
import time

import fitz  # PyMuPDF
from PIL import Image
import io
import os


def compress_pdf(input_pdf_path, output_pdf_path, image_quality=80):
    """ Уменьшить размер pdf файла. """

    # Открываем исходный PDF документ
    doc = fitz.open(input_pdf_path)
    # Новый PDF документ для сохраненных сжатых страниц
    new_doc = fitz.open()

    # Перебираем страницы pdf файла.
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        # Сжимаем изображение и сохраняем во временный файл
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=image_quality)
        temp_img_path = f"temp_img_{page_num}.jpg"
        with open(temp_img_path, "wb") as f:
            f.write(img_byte_arr.getvalue())

        # Создаем новую страницу в новом документе со сжатым изображением.
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        img_rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
        new_page.insert_image(img_rect, filename=temp_img_path)

        # Удаляем временный файл изображения
        os.remove(temp_img_path)

    # Сохраняем новый сжатый PDF
    new_doc.save(output_pdf_path)
    new_doc.close()
    doc.close()


# Пример использования
if __name__ == '__main__':
    start = time.time()

    input_pdf_path = r'C:\Users\RIMinullin\Desktop\на сжатие.pdf'
    output_pdf_path = r"C:\Users\RIMinullin\Desktop\сжатый.pdf"
    compress_pdf(input_pdf_path, output_pdf_path)
    input_pdf_path = r'C:\Users\RIMinullin\Desktop\на сжатие2.pdf'
    output_pdf_path = r"C:\Users\RIMinullin\Desktop\сжатый2.pdf"
    compress_pdf(input_pdf_path, output_pdf_path)

    elapsed_time = time.time() - start
    print(f"{elapsed_time:.3f}")
