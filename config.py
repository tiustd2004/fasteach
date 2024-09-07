import os

from sqlalchemy import create_engine

SECRET_KEY = os.environ.get("SECRET_KEY")

# Получение переменных окружения
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

# Формирование корректного URL для подключения к базе данных
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создание асинхронного движка
engine = create_engine(DATABASE_URL)
