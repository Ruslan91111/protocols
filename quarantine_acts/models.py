"""
Модель актов карантинного фитосанитарного контроля.
"""
from sqlalchemy import Column, Integer, String, Date, Float

from database.base import Base


class QuarantineAct(Base):
    """ Основная часть протокола - основные общие данные. """

    __tablename__ = 'quarantine_act'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)

    number = Column(String, nullable=False, unique=True)  # Основной номер вверху акта.
    date = Column(Date, nullable=True)  # Основная дата вверху акта.

    vehicle = Column(String, nullable=True)  # Транспортное средство.
    exporter = Column(String, nullable=True)
    importer = Column(String, nullable=True)

    name_of_prod = Column(String, nullable=True)  # Наименование подкарантинной продукции.
    certificate_number = Column(String, nullable=True)  # Фитосанитарный сертификат номер.
    certificate_date = Column(Date, nullable=True)  # Фитосанитарный сертификат дата.
    weight = Column(Float, nullable=True)  # Количество подкарантинной продукции.
