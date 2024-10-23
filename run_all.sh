#!/bin/bash

# Запускаем каждый скрипт по очереди
python -m test_task
python -m integration
python -m e2e
