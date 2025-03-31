"""
Настройки подключения к БД Postgres.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Загружаем переменные окружения из файла .env
load_dotenv()


# Настройки подключения
DB_USER = os.getenv('DB_USER')  # имя пользователя
DB_PASSWORD = os.getenv('DB_PASSWORD')  # ваш пароль
DB_HOST = os.getenv('DB_HOST')  # адрес сервера базы данных
DB_PORT = os.getenv('DB_PORT')  # порт по умолчанию для PostgreSQL
DB_NAME = os.getenv('DB_NAME')  # имя базы данных

# Строка подключения к базе данных
PROTOCOLS_DB = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Создание подключения к базе данных
protocols_engine = create_engine(PROTOCOLS_DB, echo=True)

# Фабрика сеансов, настроенная для управления транзакциями с использованием базы данных
prot_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=protocols_engine)
