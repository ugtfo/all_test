# Указываем базовый образ
FROM python:3.11-slim-buster as base

# Копируем скрипт в контейнер
COPY run_all.sh /all_test/run_all.sh
RUN chmod +x /all_test/run_all.sh  # Делаем скрипт исполняемым

# The actual dev/test image.
FROM base as test
COPY ./requirements.txt /all_test/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade -r /all_test/requirements.txt

# Assuming you run tests using pytest.
ENTRYPOINT ["python", "-m", "pytest"]
CMD ["/all_test"] 

# The actual production image.
FROM base as runtime
COPY ./requirements.txt /all_test/requirements.txt  
RUN python -m pip install --no-cache-dir --upgrade -r /all_test/requirements.txt

ENTRYPOINT ["python"]

# Указываем команду для запуска скрипта
CMD ["/all_test/run_all.sh"]
