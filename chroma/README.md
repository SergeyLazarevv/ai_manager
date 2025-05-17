Просмотр коллекций
curl http://localhost:8000/api/v1/collections
curl -s http://localhost:8000/api/v1/collections | jq .

Получить содержимое коллекции
curl -X POST http://localhost:8000/api/v1/collections/{collection_id}/get
  -H "Content-Type: application/json"
  -d '{"limit": 5}'

```
curl -X POST http://localhost:8000/api/v1/collections/{COLLECTION_ID}/get \
  -H "Content-Type: application/json" \
  -d '{"include": ["embeddings"]}' | jq .embeddings
```

Удалить коллекцию
curl -X DELETE http://localhost:8000/api/v1/collections/{collection_name}
