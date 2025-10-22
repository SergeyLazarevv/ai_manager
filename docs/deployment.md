# Deployment and Operations

## Prerequisites
- Docker and Docker Compose
- `.env` file with required secrets for `ai-service`

## Environment variables

ai-service (`config/settings.py`):
- `LLM_PROVIDER`: LLM provider key, e.g., `yandex`
- `YANDEX_OAUTH`: OAuth token to exchange for IAM token
- `YANDEX_GET_TOKEN_URL`: URL to exchange OAuth for IAM (JSON API)
- `YANDEX_LLM_URL`: YandexGPT completion endpoint URL
- `YANDEX_CATALOG_ID`: Yandex catalog ID used to build `modelUri`
- `YANDEX_API_KEY`: API key if required (not used directly in code)
- `CHROMA_HOST`: Chroma host (default `chroma-db` in Docker network)
- `CHROMA_PORT`: Chroma port (default `8000`)
- `CHROMA_TENANT`: Chroma tenant (default `default_tenant`)
- `CHROMA_DATABASE`: Chroma database (default `default_database`)

importer:
- `CHROMA_HOST` (default `chroma-db`)
- `CHROMA_PORT` (default `8000`)

chroma-ui:
- `CHROMA_HOST` (default `localhost`)
- `CHROMA_PORT` (default `8000`)

## Bringing up the stack

```bash
docker-compose up --build --remove-orphans
```

- ChromaDB REST API: `http://localhost:8000`
- ai-service: `http://localhost:3000`
- importer: `http://localhost:4000`

## Health checks
- ai-service: `GET /health`
- importer: `GET /health`

## Example workflows

### 1) Index a repository into Chroma
```bash
curl -X POST "http://localhost:4000/imports" \
  -H "Content-Type: application/json" \
  -d '{"path":"/absolute/path/to/repo"}'
```

### 2) Query with augmented context
```bash
curl -X POST http://localhost:3000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize the repo"}'
```

## Operational notes
- Initial model download (`all-MiniLM-L6-v2`) may take time and internet.
- `ai-service` caches IAM token for 1 hour via `TTLCache`.
- `VectorStore` ensures collection `crocodile` exists; adjust collection name in `llm/vector_store.py` if needed.
