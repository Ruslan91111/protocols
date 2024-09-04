"""
Модуль настройки базы данных для хранения протоколов.

Этот модуль создает соединение с базой данных SQLite, который хранит информацию в
файле 'store.database'. Он использует SQLAlchemy для управления сеансами и
определения моделей данных.

Примечания:
    - Настройка `autocommit=False` и `autoflush=False` в sessionmaker предотвращает
        автоматическое подтверждение транзакций и автоматическую очистку сеанса,
        что дает пользователю больше контроля над процессом.
"""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_DIR = Path(__file__).resolve().parent

# Путь к БД.
PROTOCOLS_DB = f'sqlite:///{DB_DIR}\protocol.database'
# Создание подключения к базе данных.
protocols_engine = create_engine(PROTOCOLS_DB, echo=True)
# Фабрика сеансов, настроенная для управления транзакциями с использованием базы данных.
prot_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=protocols_engine)
