FROM python:3.11-slim-buster as base

# Обновляем пакеты и устанавливаем необходимые зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем все файлы в контейнер
COPY . /app
WORKDIR /app

# Обновляем pip
RUN python -m pip install --upgrade pip

# Устанавливаем зависимости
RUN python -m pip install --no-cache-dir -r requirements.txt

# Делаем скрипт исполняемым
RUN chmod +x run_all.sh

# Запускаем скрипт
CMD ["./run_all.sh"]
