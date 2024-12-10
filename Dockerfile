# Используем официальный образ Python
FROM python:3.12

# Устанавливаем bash (и обновляем пакеты)
RUN apt-get update && apt-get install -y bash

# Устанавливаем рабочую директорию
WORKDIR /app

ENV PYTHONPATH=/app

# Копируем файлы в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY run_migrations.sh /app/run_migrations.sh
RUN chmod +x /app/run_migrations.sh

# Указываем команду для запуска приложения
CMD ["sh", "-c", "./run_migrations.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
