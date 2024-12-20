import PyPDF2


def remove_pdf_pages(pdf_path: str, pages_to_remove: list, output_path: str):
    """
    Удаляет указанные страницы из PDF файла и сохраняет новый файл.

    :param pdf_path: Путь к исходному PDF файлу.
    :param pages_to_remove: Список номеров страниц для удаления (индекс начинается с 0).
    :param output_path: Путь к новому PDF файлу.
    """
    # Открытие PDF файла для чтения
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Перебираем все страницы PDF файла
        for i in range(len(reader.pages)):
            if i not in pages_to_remove:
                # Если страница не в списке для удаления, добавляем её в новый файл
                writer.add_page(reader.pages[i])

        # Сохранение нового PDF файла
        with open(output_path, 'wb') as new_file:
            writer.write(new_file)


if __name__ == '__main__':
    PATH_PDF = r'C:\Users\RIMinullin\Desktop\не конвертирует\pdf\scan_20241212131828.pdf'
    OUTPUT_PDF = r'C:\Users\RIMinullin\Desktop\не конвертирует\pdf\scan_20241212131828_rm.pdf'

    remove_pdf_pages(PATH_PDF, [5, 7, 9], OUTPUT_PDF)