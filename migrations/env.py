# migrations/env.py
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models.models import metadata
# Импорт моделей


# Настройка конфигурации Alembic
config = context.config

# Получение переменных окружения и установка строки подключения
db_user = os.getenv('DB_USER', 'default_user')
db_pass = os.getenv('DB_PASS', 'default_pass')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')  # Убедитесь, что это строка, которая будет преобразована в число при необходимости
db_name = os.getenv('DB_NAME', 'default_db')

# Проверка и установка строки подключения
try:
    db_port = int(db_port)  # Преобразование порта в число
except ValueError:
    raise ValueError(f"Invalid DB_PORT value: {db_port}")

# Установка строки подключения
config.set_main_option('sqlalchemy.url', f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}")

# Настройка логирования
fileConfig(config.config_file_name)

# Метаданные базы данных
target_metadata = metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
