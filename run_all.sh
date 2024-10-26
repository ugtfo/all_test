#!/bin/bash

# Запускаем каждый скрипт по очереди
python -m tests_task &&
python -m integration &&
python -m e2e
