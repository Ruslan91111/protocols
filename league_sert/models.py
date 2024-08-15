"""
Модели для протоколов типа ЛИГА-СЕРТ.

Основная связующая сущность - MainProtocol: основные данные из протокола.
Остальные сущности - модели(подразделяются в зависимости от объекта исследований)
связаны ключами с основными данными.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
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
    air = relationship("Air", back_populates="main_prot")
    water = relationship("Water", back_populates="main_prot")


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
    indic_compl = Column(String)  # Вывод о наличии несоответствий показателей.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='prod_control')


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
    indic = Column(JSON)  # Результат исследований
    indic_compl = Column(String)  # Вывод о наличии несоответствий показателей.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='manuf_prod')


class Air(Base):
    """ Объект исследования - воздух. """
    __tablename__ = 'air'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    # Обычные поля
    sample_code = Column(String)  # Шифр пробы.
    indic = Column(JSON)  # Результат исследований
    indic_compl = Column(String)  # Вывод о наличии несоответствий показателей.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='air')


class Water(Base):
    """ Объект исследования - вода. """
    __tablename__ = 'water'

    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    test_object = Column(String)  # Объект исследований.
    sample_code = Column(String)  # Шифр пробы.
    indic = Column(JSON)  # Результаты исследований
    indic_compl = Column(String)  # Вывод о наличии несоответствий показателей.
    # Связь с основными данными.
    main_prot_id = Column(Integer, ForeignKey('main_prot.id'))
    main_prot = relationship('MainProtocol', back_populates='water')
