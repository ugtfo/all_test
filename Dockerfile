FROM python:3.11-slim-buster as base

# Обновляем пакеты и устанавливаем необходимые зависимости для psycopg2 и Allure
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    openjdk-17-jdk \
    wget && \
    wget -qO - https://dl.bintray.com/qameta/gpg.key | apt-key add - && \
    echo "deb https://dl.bintray.com/qameta/allure-deb stable main" | tee /etc/apt/sources.list.d/allure.list && \
    apt-get update && \
    apt-get install -y allure && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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
