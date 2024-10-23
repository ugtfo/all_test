# Указываем базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт в контейнер
COPY run_all.sh .

# Указываем команду для запуска скрипта
CMD ["./run_all.sh"]
