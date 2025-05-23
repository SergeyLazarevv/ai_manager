# Используем официальный образ Python
FROM python:3.11-slim

# Рабочая директория в контейнере
WORKDIR /ai-service

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код (это будет перезаписано volume mount)
COPY . .

# Открываем порт, на котором работает сервис
EXPOSE 3000

# Команда запуска сервиса
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]