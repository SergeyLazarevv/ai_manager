FROM python:3.11-slim

WORKDIR /importer

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Открываем порт, на котором работает сервис (например, FastAPI)
EXPOSE 3000

# Команда запуска сервиса
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]