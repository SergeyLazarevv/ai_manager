# Запуск: uvicorn main:app --reload

# Swagger UI: http://localhost:8000/docs

curl -X POST http://127.0.0.1:3000/query   -H "Content-Type: application/json"   -d '{"prompt": "Можешь нарисовать схему, в формате макрдаун?"}'
