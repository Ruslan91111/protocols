import itertools
import json
import re
from typing import List
import docx2txt
import pandas as pd
from docx import Document

from constants import REQUIRED_KEYS_FOR_PARSING_FIRST_PAGE

data1 = {'Номер протокола': '№13435/23-Д', 'Дата протокола': '27 декабря 2023', 'Место отбора проб': '77030', 'Дата и время отбора проб': '18.12.2023 г., И ч. 00 мин.', 'Сопроводительные документы': 'Акт отбора проб № 13435 от 18.12.2023 г.', 'Группа продукции': 'Продукция производителя', 'Наименование продукции': 'Молоко питьевое пастеризованное м. д. жира 3,2%', 'Дата производства продукции': '14.12.2023 г. Годен до 30.12.2023 г.', 'Производитель (фирма, предприятие, организация)': 'ООО «Милк Экспресс»', 'Дата проведения исследований': '18.12.2023 г.-24.12.2023 г.', 'Показатели': [{'Токсичные элементы, мг/кг:': ('Токсичные элементы, мг/кг:', 'Токсичные элементы, мг/кг:'), '- свинец': ('0,185±0,055', 'не более 0,35'), '- мышьяк': ('<0,05', 'не более 0,15'), '- кадмий': ('0,005±0,002', 'не более 0,07'), '- ртуть': ('< 0,002', 'не более 0,015'), 'Пестициды, мг/кг:': ('Пестициды, мг/кг:', 'Пестициды, мг/кг:'), '- ГХЦГ(а, р, у - изомеры)': ('<0,01', 'не более 0,5'), '- ДДТ и его метаболиты': ('<0,01', 'не более 0,02'), '-гексахлорбензол': ('<0,01', 'не более 0,01'), '- ртутьорганические': ('<0,01', 'не допускаются'), '- 2,4-Д кислота, ее соли, эфиры': ('<0,02', 'не допускаются')}, {'Количество мезофильных, аэробных и факультативно-анаэробных микроорганизмов, КОЕ/см3': ('3,0х103', 'не более 1,0x10s'), 'БГКП (колиформы)': ('не обнаружены в 0,01 см3', 'не допускаются в 0,01 см3'), 'S. aureus': ('не обнаружено в 1,0 см3', 'не допускаются в 1,0 см3'), 'L. monocytogenes': ('не обнаружено в 25 см3', 'не допускаются в 25 см3'), 'Патогенные микроорганизмы, в т.ч. сальмонеллы': ('не обнаружено в 25 см3', 'не допускаются в 25 см3')}]}
data2 = {'Номер протокола': '№13509/23-Д', 'Дата протокола': '29 декабря 2023', 'Место отбора проб': '77029', 'Дата и время отбора проб': '19.12.2023 г., 08 ч. 55 мин.', 'Сопроводительные документы': 'Акт отбора проб № 13509 от 19.12.2023 г.', 'Группа продукции': 'Производство магазина', 'Наименование продукции': 'Улитка греческая косичка с сыром и картофелем', 'Дата производства продукции': '19.12.2023 г. Срок годности 24 часа', 'Производитель (фирма, предприятие, организация)': 'АО «Дикси ЮГ»', 'Дата проведения исследований': '19.12.2023 г.-25.12.2023 г.', 'Показатели': [{'Массовая доля сорбиновой кислоты, мг/кг': ('<20', 'не более 2000'), 'Массовая доля бензойной кислоты, мг/кг': ('<20', '-')}, {'Токсичные элементы, мг/кг:': ('Токсичные элементы, мг/кг:', 'Токсичные элементы, мг/кг:'), '- свинец': ('0,048±0,019', 'не более 0,35'), '- мышьяк': ('<0,05', 'не более 0,15'), '- кадмий': ('0,011±0,004', 'не более 0,07'), '- ртуть': ('< 0,002', 'не более 0,015'), 'Пестициды, мг/кг:': ('Пестициды, мг/кг:', 'Пестициды, мг/кг:'), '- ГХЦГ(а, Р, у - изомеры)': ('<0,01', 'не более 0,5'), '- ДДТ и его метаболиты': ('<0,01', 'не более 0,02'), '- гексахлорбензол': ('<0,01', 'не более 0,01'), '- ртутьорганические': ('<0,01', 'не допускаются'), '- 2,4-Д кислота, ее соли, эфиры': ('<0,02', 'не допускаются')}]}
data3 ={'Номер протокола': '№13432/23-Д', 'Дата протокола': '27 декабря 2023', 'Место отбора проб': '90344', 'Дата и время отбора проб': '18.12.2023 г., 14 ч. 10 мин.', 'Сопроводительные документы': 'Акт отбора проб № 13432 от 18.12.2023 г.', 'Группа продукции': 'Производство магазина', 'Наименование продукции': 'Улитка греческая «Косичка» с курицей, рисом и овощами', 'Дата производства продукции': '27.09.2023 г. Годен до 27.09.2024 г.', 'Производитель (фирма, предприятие, организация)': 'АО «Дикси ЮГ» №90344', 'Дата проведения исследований': '18.12.2023 г.-24.12.2023 г.', 'Показатели': [{'Массовая доля сорбиновой кислоты, мг/кг': ('90,2±10,0', 'не более 2000'), 'Массовая доля бензойной кислоты, мг/кг': ('<20', '-')}]}


datas = [data1, data2, data3]

columns = ['Номер протокола', 'Дата протокола', 'Место отбора проб',
           'Дата и время отбора проб', 'Сопроводительные документы',
           'Группа продукции', 'Наименование продукции',
           'Дата производства продукции',
           'Производитель (фирма, предприятие, организация)',
           'Дата проведения исследований', 'Показатель', 'Значение']


def make_row_with_multindex(data):
    protocol_num = data['Номер протокола']
    protocol_date = data['Дата протокола']
    sampling_site = data['Место отбора проб']
    sampling_date_and_time = data['Дата и время отбора проб']
    accompanying_documents = data['Сопроводительные документы']

    product_group = data['Группа продукции']

    name_of_product = data['Наименование продукции']
    production_date = data['Дата производства продукции']
    manufacturer = data['Производитель (фирма, предприятие, организация)']
    date_of_research = data['Дата проведения исследований']
    indicators = data['Показатели']
    rows = [(protocol_num, protocol_date, sampling_site, sampling_date_and_time, accompanying_documents, product_group,
             name_of_product, production_date, manufacturer, date_of_research, key, value)
            for key, value in indicators[0].items()]
    df = pd.DataFrame(rows, columns=columns)
    # df.set_index(columns[:-2], inplace=True)
    return df


def make_one_df(datas):
    new_df = pd.DataFrame(columns=columns)

    for data in datas:
        df = make_row_with_multindex(data)

        new_df = pd.concat([new_df, df])
    new_df.set_index(columns[:-1], inplace=True)
    new_df.to_excel(r'x.xlsx')


make_one_df(datas)
