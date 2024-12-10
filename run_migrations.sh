set -e  # Прерывать выполнение скрипта при ошибке

echo "Running Alembic migrations..."

# Генерация ревизии (если нужно)
alembic revision --autogenerate -m "init database" || echo "Revision already exists, skipping..."

# Применение миграций
alembic upgrade head

echo "Alembic migrations completed!"
