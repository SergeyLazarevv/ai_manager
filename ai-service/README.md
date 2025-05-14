# Запуск: uvicorn main:app --reload

# Swagger UI: http://localhost:8000/docs



curl -X POST http://127.0.0.1:8000/query
  -H "Content-Type: application/json"
  -d '{"text": "Привет, как дела?"}'
