FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
RUN pip install chromadb==0.5.3

# Копирование скрипта
COPY init_collections.py /app/init_collections.py