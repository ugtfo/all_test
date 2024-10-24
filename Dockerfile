FROM python:3.11-slim-buster as base

# Обновляем пакеты и устанавливаем необходимые зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    openjdk-17-jdk \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Allure
RUN wget -q -O allure.zip "https://github.com/allure-framework/allure2/releases/download/2.14.0/allure-2.30.0.zip" && \
    unzip allure.zip -d /opt && \
    ln -s /opt/allure-2.30.0/bin/allure /usr/bin/allure && \
    rm allure.zip

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
