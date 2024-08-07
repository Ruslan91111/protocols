data_preparation

data_preparation — это пакет, который предоставляет инструменты для получения и преобразования данных из файла формата Word. Пакет состоит из нескольких модулей, которые отвечают за различные этапы обработки данных, начиная от чтения исходного файла и заканчивая записью результатов в базу данных.

Структура Пакета:
    
Модули:

    - value_processor:
        Модуль для преобразования переданного значения в вид, подходящий для последующего сравнения результатов исследований и норм.

    - comparator: 
        Модуль для сравнения результатов исследований и норм.

    - add_conclusions:
        Модуль для добавления в каждую таблицу из переданных данных выводов о соответствии результатов исследования нормам для каждого конкретного показателя и всей таблицы в целом.
    
    - file_parser:
        Модуль для парсинга файлов формата Word. Код модуля обрабатывает Word файл и получает из него нужные данные, подлежащие передаче для дальнейшей работы по преобразованию и сравнению. Необходимые для дальнейшей работы данные становятся свойствами объекта класса MainDataGetter. Модуль содержит классы и методы, направленные на извлечение данных.

    - merge_tables:
        Модуль для финальной обработки данных из таблиц. Код модуля объединяет таблицы показателей в соответствующую таблицу образцов, удаляет лишние данные, определяет тип таблицы и прописывает его в ключе таблицы.

    - common:
        Модуль с кодом и данными, которые используются более, чем одним модулем.

    - launch_data_preparation:
        Модуль содержит функцию запуска всего кода пакета data_preparation.