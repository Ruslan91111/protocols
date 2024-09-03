from sqlalchemy import create_engine, text

from database.db_config import protocols_engine

import pandas as pd

sql_query = """
SELECT id AS id_в_бд, number AS номер_основного_протокола, 
    sampling_site AS место_отбора_проб, sampling_date AS дата_отбора_проб  
FROM main_prot
    LEFT

"""


sql_query_2 = """
-- Продукция изготовителя
SELECT 
    mt.id AS id_в_бд, 
    mt.number AS номер_основного_протокола, 
    mt.sampling_site AS место_отбора_проб, 
    mt.sampling_date AS дата_отбора_проб,
    'Продукция_производителя' AS Тип_исследования,
    mp.name_indic AS Наименование_показателя,
    mp.result AS Результат,
    mp.norm AS Норма,
    mp.conformity_main AS Соответствие_нормам_основной_показатель,
    mp.conformity_deviation AS Соответствие_нормам_показатель_с_отклонением,
    mp.norm_doc AS Нормативные_документы,
    
    NULL AS Параметр,    
    NULL AS Единица_измерения,    
    NULL AS номер_протокола_производственного_контроля,    
    NULL AS Дата_протокола_производственного_контроля,    
    NULL AS Акт_производственного_контроля,    
    NULL AS Адрес_отбора_проб_производственного_контроля,    
    NULL AS Текст_заключения,    
    NULL AS Наличие_нарушений_в_заключении,
    
    mp.sample_code AS Шифр_проб,
    mp.prod_name AS Наименование_товара,
    mp.prod_date AS Дата_производства,
    mp.manuf AS Изготовитель
        
FROM main_prot mt
JOIN manuf_prod mp ON mt.id = mp.main_prot_id

UNION ALL

-- Производство магазина
SELECT
    mt.id AS id_в_бд, 
    mt.number AS номер_основного_протокола, 
    mt.sampling_site AS место_отбора_проб, 
    mt.sampling_date AS дата_отбора_проб,
    
    'Производство_магазина' AS Тип_исследования,
    
    sp.name_indic AS Наименование_показателя,
    sp.result AS Результат,
    sp.norm AS Норма,
    sp.conformity_main AS Соответствие_нормам_основной_показатель,
    sp.conformity_deviation AS Соответствие_нормам_показатель_с_отклонением,
    sp.norm_doc AS Нормативные_документы,
    
    NULL AS Параметр,    
    NULL AS Единица_измерения,    
    NULL AS номер_протокола_производственного_контроля,    
    NULL AS Дата_протокола_производственного_контроля,    
    NULL AS Акт_производственного_контроля,    
    NULL AS Адрес_отбора_проб_производственного_контроля,    
    NULL AS Текст_заключения,    
    NULL AS Наличие_нарушений_в_заключении,
    
    sp.sample_code AS Шифр_проб,
    sp.prod_name AS Наименование_товара,
    sp.prod_date AS Дата_производства,
    sp.manuf AS Изготовитель
      
FROM main_prot mt
JOIN store_prod sp ON mt.id = sp.main_prot_id

UNION ALL

-- Воздух
SELECT
    mt.id AS id_в_бд, 
    mt.number AS номер_основного_протокола, 
    mt.sampling_site AS место_отбора_проб, 
    mt.sampling_date AS дата_отбора_проб,
    'Воздух' AS Тип_исследования,
    air.name_indic AS Наименование_показателя,
    air.result AS Результат,
    air.norm AS Норма,
    air.conformity_main AS Соответствие_нормам_основной_показатель,
    air.conformity_deviation AS Соответствие_нормам_показатель_с_отклонением,
    air.norm_doc AS Нормативные_документы,
    
    NULL AS Параметр,    
    NULL AS Единица_измерения,    
    NULL AS номер_протокола_производственного_контроля,    
    NULL AS Дата_протокола_производственного_контроля,    
    NULL AS Акт_производственного_контроля,    
    NULL AS Адрес_отбора_проб_производственного_контроля,    
    NULL AS Текст_заключения,    
    NULL AS Наличие_нарушений_в_заключении,
    
    air.sample_code AS Шифр_проб,
    NULL AS Наименование_товара,      
    NULL AS Дата_производства,       
    NULL AS Изготовитель             
      
FROM main_prot mt
JOIN air ON mt.id = air.main_prot_id

UNION ALL

-- Вода
SELECT
    mt.id AS id_в_бд, 
    mt.number AS номер_основного_протокола, 
    mt.sampling_site AS место_отбора_проб, 
    mt.sampling_date AS дата_отбора_проб,
    
    'Вода' AS Тип_исследования,
    
    water.name_indic AS Наименование_показателя,
    water.result AS Результат,
    water.norm AS Норма,
    water.conformity_main AS Соответствие_нормам_основной_показатель,
    water.conformity_deviation AS Соответствие_нормам_показатель_с_отклонением,
    
    water.norm_doc AS Нормативные_документы,
    
    NULL AS Параметр,    
    NULL AS Единица_измерения,    
    NULL AS номер_протокола_производственного_контроля,    
    NULL AS Дата_протокола_производственного_контроля,    
    NULL AS Акт_производственного_контроля,    
    NULL AS Адрес_отбора_проб_производственного_контроля,    
    NULL AS Текст_заключения,    
    NULL AS Наличие_нарушений_в_заключении,  
    
    water.sample_code AS Шифр_проб,
    
    NULL AS Наименование_товара,      
    NULL AS Дата_производства,        
    NULL AS Изготовитель               

FROM main_prot mt
JOIN water ON mt.id = water.main_prot_id

UNION ALL

-- Смывы
SELECT
    mt.id AS id_в_бд, 
    mt.number AS номер_основного_протокола, 
    mt.sampling_site AS место_отбора_проб, 
    mt.sampling_date AS дата_отбора_проб,
    
    'Смывы' AS Тип_исследования,

    washings.name_indic AS Наименование_показателя,
    washings.result AS Результат,
    washings.norm AS Норма,
    washings.conformity_main AS Соответствие_нормам_основной_показатель,
    washings.conformity_deviation AS Соответствие_нормам_показатель_с_отклонением,    
    washings.norm_doc AS Нормативные_документы,
    
    NULL AS Параметр,    
    NULL AS Единица_измерения,    
    NULL AS номер_протокола_производственного_контроля,    
    NULL AS Дата_протокола_производственного_контроля,    
    NULL AS Акт_производственного_контроля,    
    NULL AS Адрес_отбора_проб_производственного_контроля,    
    NULL AS Текст_заключения,    
    NULL AS Наличие_нарушений_в_заключении,
    
    NULL AS Шифр_проб, 
    NULL AS Наименование_товара,      
    NULL AS Дата_производства,        
    NULL AS Изготовитель               
      
FROM main_prot mt
JOIN washings ON mt.id = washings.main_prot_id
    
UNION ALL

-- Производственный контроль
SELECT
    mt.id AS id_в_бд, 
    mt.number AS номер_основного_протокола, 
    mt.sampling_site AS место_отбора_проб, 
    mt.sampling_date AS дата_отбора_проб,
    
    'Производственный контроль' AS Тип_исследования,
    prod_control.name_indic AS Наименование_показателя,
    prod_control.result AS Результат,
    prod_control.norm AS Норма,
    prod_control.conformity_main AS Соответствие_нормам_основной_показатель,
    prod_control.conformity_deviation AS Соответствие_нормам_показатель_с_отклонением,    
    
    NULL AS Нормативные_документы,
   
    prod_control.parameter AS Параметр,    
    prod_control.unit AS Единица_измерения,    
    prod_control.number AS номер_протокола_производственного_контроля,    
    prod_control.date AS Дата_протокола_производственного_контроля,    
    prod_control.act AS Акт_производственного_контроля,    
    prod_control.address AS Адрес_отбора_проб_производственного_контроля,    
    prod_control.conclusion AS Текст_заключения,    
    prod_control.conclusion_compl AS Наличие_нарушений_в_заключении,   
     
    NULL AS Шифр_проб,
    NULL AS Наименование_товара,      
    NULL AS Дата_производства,        
    NULL AS Изготовитель     
        
FROM main_prot mt
JOIN prod_control ON mt.id = prod_control.main_prot_id  

"""




# Создание соединения и выполнение запроса
with protocols_engine.connect() as connection:
    # Пример сырого SQL-запроса для выборки данных
    result = connection.execute(text(sql_query_2))

    # Получение всех строк результата
    rows = result.fetchall()

    # Печать результатов выборки
    for row in rows:
        print(row)

    df = pd.DataFrame(rows)
    df = df.sort_values(by='id_в_бд', ascending=True)
    df.to_excel('probe.xlsx', index=False)