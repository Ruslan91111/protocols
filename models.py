""" Модели данных."""
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Store(Base):
    """Модель - магазины"""
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)  # Уникальный номер магазина
    address = Column(String, nullable=False)  # Адрес магазина
    protocols = relationship("Protocol", back_populates="store")  # Связь с таблицей протоколы

    def __repr__(self):
        """Представление экземпляров класса"""
        return f"\n<Магазин(номер={self.id}, адрес='{self.address}')>"


class Protocol(Base):
    """Модель - протоколы"""
    __tablename__ = 'protocols'
    # Primary key - составной на два поля.
    number = Column(String, primary_key=True, nullable=False)
    date = Column(String, primary_key=True, nullable=False)
    # Foreign Key - store - связь с таблицей магазины
    store_id = Column(Integer, ForeignKey('stores.id'))
    # Определяем отношение к модели Store
    store = relationship("Store", back_populates="protocols")

    sampling_datetime = Column(String, nullable=True)
    accompanying_documents = Column(String, nullable=True)
    product_type = Column(String, nullable=True)
    name_of_product = Column(String, nullable=True)
    production_date = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    date_of_test = Column(String, nullable=True)
    indicators = Column(JSON)
    compliance_with_standards = Column(String, nullable=True)

    def __repr__(self):
        """Представление экземпляров класса"""
        return (
            f"<Номер протокола={self.number},\n"
            f"\tДата протокола={self.date},\n"
            f"\tМесто отбора проб={self.store_id},\n"
            f"\tАдрес магазина={self.store.address if self.store else 'None'},\n"
            f"\tСопроводительные документы={self.accompanying_documents},\n"
            f"\tГруппа продукции={self.product_type},\n"
            f"\tНаименование продукции={self.name_of_product},\n"
            f"\tДата производства продукции={self.production_date},\n"
            f"\tПроизводитель (фирма, предприятие, организация)={self.manufacturer},\n"
            f"\tДата проведения исследований={self.date_of_test},\n"
            f"\tПоказатели={self.indicators},\n"
            f"\tСоответствие нормам={self.compliance_with_standards}>\n"
        )
