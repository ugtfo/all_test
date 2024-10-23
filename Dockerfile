FROM python:3.11-slim-buster as base

COPY . ./
RUN chmod +x run_all.sh

RUN python -m pip install --no-cache-dir -r requirements.txt
