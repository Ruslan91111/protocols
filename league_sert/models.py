"""
Модели для протоколов типа ЛИГА-СЕРТ.

Основная связующая сущность - MainProtocol: основные данные из протокола.
Остальные сущности - модели(подразделяются в зависимости от объекта исследований)
связаны ключами с основными данными.
"""
from abc import ABC

import pandas as pd
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship

from database.base import Base


class MainProtocol(Base):
    """ Основная часть протокола - основные общие данные. """

    __tablename__ = 'main_prot'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    # Обычные поля
    number = Column(String, nullable=True, unique=True)
    date = Column(String, nullable=True)
    sampling_site = Column(String, nullable=True)  # Место отбора проб.
    sampling_date = Column(String, nullable=True)  # Дата и время отбора проб.

    # Связи с другими сущностями: различными составляющими протокола
    prod_control = relationship("ProdControl", back_populates="main_prot")
    manuf_prod = relationship("ManufProd", back_populates="main_prot")
    store_prod = relationship("StoreProd", back_populates="main_prot")
    air = relationship("Air", back_populates="main_prot")
    water = relationship("Water", back_populates="main_prot")
    washings = relationship("Washings", back_populates="main_prot")

    def to_df(self):
        data = {
            'id основного протокола': [self.id],
            'Номер основного протокола': [self.number],
            'Дата основного протокола': [self.date],
            'Место отбора проб': [self.sampling_site],
            'Дата и время отбора проб': [self.sampling_date],
        }
        return pd.DataFrame(data)

    def return_row(self):
        data = [self.id, self.number, self.date, self.sampling_site, self.sampling_date]
        return pd.DataFrame(data)


class ProdControl(Base):
    """ Протокол измерений по производственному контролю  """
    __tablename__ = 'prod_control'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    # Обычные поля
    number = Column(String)
    date = Column(String)
    act = Column(String)  # Акт и дата проведения измерений.
    address = Column(String)  # Адрес проведения измерений.
    conclusion = Column(String)  # Заключение
    conclusion_compl = Column(String)  # Установлены ли нарушения в заключении

    indic = Column(JSON)  # Результаты измерений.
    violat_main = Column(Boolean)  # Вывод о наличии несоответствий показателей.
    violat_dev = Column(Boolean)  # Вывод о наличии несоответствий для чисел с отклонением.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='prod_control')

    def return_row(self):
        data = ['Производственный контроль', self.number, self.date,
                self.date, self.act, self.address, self.conclusion,
                self.conclusion_compl, self.violat_main, self.violat_dev]
        prod_control_indics = [[k, v['parameter'],
                                v['unit'],
                                v['result'],
                                v['norm'],
                                v['conformity_main'],
                                v['conformity_deviation'],
                                ] for k, v in self.indic.items()]
        return data.append(prod_control_indics)

    def to_df(self):
        data = {
            'Номер протокола произв контроля': [self.number],
            'Дата протокола произв контроля': [self.date],
            'Акт произв контроля': [self.act],
            'Адрес измерений произв контроля': [self.address],
            'Заключение произв контроля': [self.conclusion],
            'Нарушения в заключении произв контроля': [self.conclusion_compl],
            'Соответствие нормам основных чисел произв контроля': [self.violat_main],
            'Соответствие нормам чисел с отклонением произв контроля': [self.violat_dev],
        }
        df1 = pd.DataFrame(data)

        # Обработка данных
        records = []
        for record in self.indic:
            for key, value in record.items():
                if key != 'violations_of_norms':
                    value['Место измерения произв контроля'] = key
                    records.append(value)

        # Создание DataFrame
        df2 = pd.DataFrame(records,
                           columns=[
                               'Место измерения произв контроля',
                               'parameter',
                               'unit',
                               'result',
                               'norm',
                               'conformity_main',
                               'conformity_deviation'
                           ])

        df2.columns = [
            'Место измерения произв контроля',
            'Параметр произв контроля',
            'Единица измерений произв контроля',
            'Результат измерений произв контроля',
            'Нормы для показателей произв контроля',
            'Соответствие результата нормам произв контроля',
            'Соответствие результата с отклонением нормам произв контроля'
        ]

        result = pd.concat([df1, df2], axis=1)
        return result


class ManufProd(Base):
    """ Данные о пробе - продукция производителя. """
    __tablename__ = 'manuf_prod'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    # Обычные поля
    sample_code = Column(String)  # Шифр пробы.
    prod_name = Column(String)  # Наименования продукции.
    prod_date = Column(String)  # Дата производства продукции
    manuf = Column(String)  # Производитель.
    indic = Column(JSON)  # Результаты измерений.
    violat_main = Column(Boolean)  # Вывод о наличии несоответствий показателей.
    violat_dev = Column(Boolean)  # Вывод о наличии несоответствий для чисел с отклонением.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='manuf_prod')

    def to_df(self):
        data = {
            'Шифр пробы продукция производства': [self.sample_code],
            'Наименование продукции производства': [self.prod_name],
            'Дата производства продукция производства': [self.prod_date],
            'Производитель': [self.manuf],
            'Соответствие нормам основных чисел продукция производства': [self.violat_main],
            'Соответствие нормам чисел с отклонением продукция производства': [self.violat_dev],
        }
        df1 = pd.DataFrame(data)

        # Обработка данных
        records = []
        for record in self.indic:
            for key, value in record.items():
                if key != 'violations_of_norms':
                    value['Показатель продукция производства'] = key
                    records.append(value)

        # Создание DataFrame
        df2 = pd.DataFrame(records,
                           columns=[
                               'Показатель продукция производства',
                               'result',
                               'norm',
                               'norm_doc',
                               'conformity_main',
                               'conformity_deviation'
                           ])
        df2.columns = [
            'Показатель продукция производства',
            'Результат исследований продукция производства',
            'Нормы продукция производства',
            'Нормативные документы продукция производства',
            'Соответствие результата нормам продукция производства',
            'Соответствие результата нормам с отклонением продукция производства'
        ]

        result = pd.concat([df1, df2], axis=1)
        return result


class StoreProd(Base):
    """ Данные о пробе - производство магазина. """
    __tablename__ = 'store_prod'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)

    # Обычные поля
    sample_code = Column(String)  # Шифр пробы.
    prod_name = Column(String)  # Наименования продукции.
    prod_date = Column(String)  # Дата производства продукции
    manuf = Column(String)  # Производитель.

    indic = Column(JSON)  # Результаты измерений.
    violat_main = Column(Boolean)  # Вывод о наличии несоответствий показателей.
    violat_dev = Column(Boolean)  # Вывод о наличии несоответствий для чисел с отклонением.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='store_prod')

    def to_df(self):
        data = {
            'Шифр пробы производство магазина': [self.sample_code],
            'Наименование производство магазина': [self.prod_name],
            'Дата производства производство магазина': [self.prod_date],
            'Производитель производство магазина': [self.manuf],
            'Соответствие нормам основных чисел производство магазина': [self.violat_main],
            'Соответствие нормам чисел с отклонением производство магазина': [self.violat_dev],
        }
        df1 = pd.DataFrame(data)

        # Обработка данных
        records = []
        for record in self.indic:
            for key, value in record.items():
                if key != 'violations_of_norms':
                    value['Показатель производство магазина'] = key
                    records.append(value)

        # Создание DataFrame
        df2 = pd.DataFrame(records,
                           columns=[
                               'Показатель производство магазина',
                               'result',
                               'norm',
                               'norm_doc',
                               'conformity_main',
                               'conformity_deviation'
                           ])
        df2.columns = [
            'Показатель производство магазина',
            'Результат исследований производство магазина',
            'Нормы производство магазина',
            'Нормативные документы производство магазина',
            'Соответствие результата нормам производство магазина',
            'Соответствие результата нормам с отклонением производство магазина'
        ]

        result = pd.concat([df1, df2], axis=1)
        return result


class Air(Base):
    """ Объект исследования - воздух. """
    __tablename__ = 'air'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    # Обычные поля
    sample_code = Column(String)  # Шифр пробы.
    indic = Column(JSON)  # Результат исследований
    violat_main = Column(Boolean)  # Вывод о наличии несоответствий показателей.
    violat_dev = Column(Boolean)  # Вывод о наличии несоответствий для чисел с отклонением.

    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='air')

    def return_row(self):
        data = ['Воздух', self.sample_code, self.violat_main, self.violat_dev]
        indics = [[k,
                   v['result'],
                   v['norm'],
                   v['norm_doc'],
                   v['conformity_main'],
                   v.get('conformity_deviation', '-'),
                   ] for k, v in self.indic.items()]
        return data.append(indics)

    def to_df(self):
        data = {
            'Шифр пробы воздух': [self.sample_code],
            'Соответствие нормам основных чисел воздух': [self.violat_main],
            'Соответствие нормам чисел с отклонением воздух': [self.violat_dev],
        }
        df1 = pd.DataFrame(data)

        # Обработка данных
        records = []
        for record in self.indic:
            for key, value in record.items():
                if key != 'violations_of_norms':
                    value['Показатель воздух'] = key
                    records.append(value)

        # Создание DataFrame
        df2 = pd.DataFrame(records,
                           columns=[
                               'Показатель воздух',
                               'result',
                               'norm',
                               'norm_doc',
                               'conformity_main',
                               'conformity_deviation'])
        df2.columns = [
            'Показатель воздух',
            'Результат исследований воздух',
            'Нормы воздух',
            'Нормативные документы воздух',
            'Соответствие результата нормам чисел воздух',
            'Соответствие результата нормам с отклонением воздух'
        ]
        result = pd.concat([df1, df2], axis=1)
        return result


class Water(Base):
    """ Объект исследования - вода. """
    __tablename__ = 'water'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    test_object = Column(String)  # Объект исследований.
    sample_code = Column(String)  # Шифр пробы.
    indic = Column(JSON)  # Результаты измерений.
    violat_main = Column(Boolean)  # Вывод о наличии несоответствий показателей.
    violat_dev = Column(Boolean)  # Вывод о наличии несоответствий для чисел с отклонением.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='water')

    def to_df(self):
        data = {
            'Объект исследования вода': [self.test_object],
            'Шифр пробы продукция вода': [self.sample_code],
            'Соответствие нормам основных чисел вода': [self.violat_main],
            'Соответствие нормам чисел с отклонением вода': [self.violat_dev],
        }
        df1 = pd.DataFrame(data)

        # Обработка данных
        records = []
        for record in self.indic:
            for key, value in record.items():
                if key != 'violations_of_norms':
                    value['Показатель вода'] = key
                    records.append(value)

        # Создание DataFrame
        df2 = pd.DataFrame(records,
                           columns=[
                               'Показатель вода',
                               'result',
                               'norm',
                               'norm_doc',
                               'conformity_main',
                               'conformity_deviation'
                           ])
        df2.columns = [
            'Показатель вода',
            'Результат исследований вода',
            'Нормы вода',
            'Нормативные документы',
            'Соответствие результат нормам вода',
            'Соответствие результата нормам с отклонением вода'
        ]
        result = pd.concat([df1, df2], axis=1)
        return result


class Washings(Base):
    """ Объект исследования - Смывы. """
    __tablename__ = 'washings'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    indic = Column(JSON)  # Результаты измерений.
    violat_main = Column(Boolean)  # Вывод о наличии несоответствий показателей.
    violat_dev = Column(Boolean)  # Вывод о наличии несоответствий для чисел с отклонением.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='washings')

    def to_df(self):
        data = {
            'Объект исследования смывы': ['Смывы'],
            'Соответствие нормам основных чисел смывы': [self.violat_main],
            'Соответствие нормам чисел с отклонением смывы': [self.violat_dev],
        }
        df1 = pd.DataFrame(data)

        # Обработка данных
        records = []
        for record in self.indic:
            for key, value in record.items():
                if key != 'violations_of_norms':
                    value['Показатель смывы'] = key
                    records.append(value)

        # Создание DataFrame
        df2 = pd.DataFrame(records,
                           columns=[
                               'Показатель смывы',
                               'result',
                               'norm',
                               'norm_doc',
                               'conformity_main',
                               'conformity_deviation'])

        df2.columns = [
            'Показатель смывы',
            'Результат исследований смывы',
            'Нормы смывы',
            'Нормативные документы смывы',
            'Соответствие результата нормам смывы',
            'Соответствие результата нормам с отклонением смывы'
        ]
        result = pd.concat([df1, df2], axis=1)
        return result
