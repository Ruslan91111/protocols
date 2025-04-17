""" Базовый класс для определения моделей,
который позволяет использовать декларативный стиль. """
from sqlalchemy.orm import declarative_base


Base = declarative_base()
