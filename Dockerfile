# Указываем базовый образ
# Make sure all layers are based on the same python version.
FROM python:3.12-slim-buster as base

# Копируем скрипт в контейнер
COPY run_all.sh /all_test/run_all.sh
RUN chmod +x /all_test/run_all.sh  # Делаем скрипт исполняемым

# The actual dev/test image.
# This is where you can install additional dev/test requirements.
FROM base as test
COPY ./requirements.txt /all_test/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Assuming you run tests using pytest.
ENTRYPOINT ["python", "-m", "pytest"]
CMD ["/all_test"] 

# The actual production image.
FROM base as runtime
COPY ./requirements.txt /all_test/requirements.txt  
RUN python -m pip install --no-cache-dir --upgrade -r /all_test/requirements.txt

ENTRYPOINT ["python"]

# Указываем команду для запуска скрипта
CMD ["/all_test/run_all.sh"]  # Убедитесь, что run_all.sh находится по этому пути
