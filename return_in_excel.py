import pandas as pd
from models import Protocol

COLUMNS_FOR_SAVE_TO_EXCEL = [
    'Номер протокола',
    'Дата протокола',
    'Код магазина',
    'Адрес магазина',
    'Дата и время отбора проб',
    'Сопроводительные документы',
    'Группа продукции',
    'Наименование продукции',
    'Дата производства продукции',
    'Производитель (фирма, предприятие, организация)',
    'Дата проведения исследований',
    'Нарушение норм в протоколе',
    'Показатель',
    'Значение',
    'Требования НД',
    'Нарушения норм'
]


def make_dataframe_from_a_protocol(protocol_data: Protocol) -> pd.DataFrame:
    """ Получить на вход объект протокол, преобразовать и вернуть DataFrame. """

    rows_for_dataframe = []
    for indicator in protocol_data.indicators:
        # Формируем строку на каждый показатель в поле показатели - Protocol.indicators
        for key, value in protocol_data.indicators[0].items():
            print(protocol_data.number)
            new_row = [
                protocol_data.number,
                protocol_data.date,
                protocol_data.store_id,

                # Проверка наличия адреса магазина в БД.
                protocol_data.store.address
                if hasattr(protocol_data.store, 'address') and
                   protocol_data.store.address is not None
                else 'адрес магазина отсутствует в Базе Данных',

                protocol_data.sampling_datetime,
                protocol_data.accompanying_documents,
                protocol_data.product_type,
                protocol_data.name_of_product,
                protocol_data.production_date,
                protocol_data.manufacturer,
                protocol_data.date_of_test,
                protocol_data.compliance_with_standards,
                # работа с полем в показателях
                key, value[0],
                value[1],
                'соответствуют' if value[2] else 'не соответствуют'
            ]
            rows_for_dataframe.append(new_row)

    df = pd.DataFrame(rows_for_dataframe, columns=COLUMNS_FOR_SAVE_TO_EXCEL)
    return df


def make_one_df_from_protocols(protocols_from_db, name_of_result_file):
    """ Подготовить данные из БД, протоколы в виде DataFrame для записи в xlsx файл. """
    list_of_dataframes = []
    # Перебираем протоколы в полученных из БД, преобразовываем в DataFrame и добавляем в список
    for data in protocols_from_db:
        df = make_dataframe_from_a_protocol(data)
        list_of_dataframes.append(df)

    # Объединяем все DataFrame за один раз, устанавливаем индекс и записываем в словарь.
    result_df = pd.concat(list_of_dataframes, ignore_index=True)
    result_df.set_index(COLUMNS_FOR_SAVE_TO_EXCEL[:-3], inplace=True)
    result_df.to_excel(name_of_result_file)
