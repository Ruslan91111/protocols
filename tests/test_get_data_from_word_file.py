import pytest

from get_data_from_word_file import WordFileParser


FILE_1 = r'.\word_files\file_1.docx'
FILE_2 = r'.\word_files\file_2.docx'
FILE_3 = r'.\word_files\file_3.docx'


@pytest.mark.parametrize("file, expected_data",
                         [(r".\word_files\file_1.docx", "data_from_word_file_1"),
                          (r".\word_files\file_2.docx", "data_from_word_file_2"),
                          (r".\word_files\file_3.docx", "data_from_word_file_3")])
def test_received_data_from_word_file(request, file, expected_data):
    expected_data_from_word_file = request.getfixturevalue(expected_data)  # Ожидаемые данные из БД
    word_parser = WordFileParser(file)
    received_data = word_parser.get_all_required_data_from_word_file()
    assert received_data == expected_data_from_word_file
