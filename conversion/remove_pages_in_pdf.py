import PyPDF2


def remove_pdf_pages(pdf_path: str, pages_to_remove: list):
    """ Удаляет указанные страницы из PDF файла и сохраняет новый файл. """
    output_path = pdf_path.replace('.pdf', '_без_страниц.pdf')

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
    PATH_PDF = r'C:\Users\RIMinullin\Desktop\2024\77147 31.01.2024.pdf'

    remove_pdf_pages(PATH_PDF, [3,5,7,9])