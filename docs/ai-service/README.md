# ai-service Documentation

FastAPI application providing a query endpoint that augments prompts with relevant context from ChromaDB and calls YandexGPT.

## Base URL
- Local (Docker): `http://localhost:3000`

## Environment
Reads configuration via `config/settings.py` from `.env`/environment variables:
- `LLM_PROVIDER` (str)
- `YANDEX_OAUTH` (str)
- `YANDEX_GET_TOKEN_URL` (str)
- `YANDEX_LLM_URL` (str)
- `YANDEX_CATALOG_ID` (str)
- `YANDEX_API_KEY` (str)
- `CHROMA_HOST` (default `chroma-db`)
- `CHROMA_PORT` (default `8000`)
- `CHROMA_TENANT` (default `default_tenant`)
- `CHROMA_DATABASE` (default `default_database`)

## API

### GET `/health`
Health check.

Response 200
```json
{"status": "ok"}
```

### POST `/query`
Runs an augmented query: fetches relevant context from ChromaDB, constructs a prompt, invokes YandexGPT, and returns model output with usage.

Request body
```json
{
  "prompt": "Explain the repository structure"
}
```

Success response 200
```json
{
  "body": "...model answer...",
  "model_version": "...",
  "input_text_tokens": "...",
  "completion_tokens": "...",
  "total_tokens": "..."
}
```

Errors
- 500: Internal error (details in `detail`)

cURL example
```bash
curl -X POST http://localhost:3000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Можешь нарисовать схему, в формате макрдаун?"}'
```

## Python client usage

```python
import requests

resp = requests.post(
    "http://localhost:3000/query",
    json={"prompt": "Summarize project services"},
    timeout=60,
)
resp.raise_for_status()
print(resp.json()["body"])
```

## Internal modules reference

### `schemas.py`
- `QueryRequest`:
  - Fields: `prompt: str`
- `QueryResponse`:
  - Fields: `body: str`, `model_version: str`, `input_text_tokens: str`, `completion_tokens: str`, `total_tokens: str`

### `llm/base.py`
- `BaseLLMClient`
  - Abstract `query(prompt: str) -> str`

### `llm/client.py`
- `Client(settings: Settings)`
  - Uses `YandexGPTRequest` and `VectorStore`
  - Token caching via `cachetools.TTLCache`
- `get_token() -> str`
  - Returns cached IAM token or fetches a new one
- `fetch_new_token() -> str`
  - Calls `YANDEX_GET_TOKEN_URL` with `YANDEX_OAUTH`
- `query(prompt: str) -> dict`
  - Retrieves vector context, formats prompt, calls `YANDEX_LLM_URL`, returns dict compatible with `QueryResponse`

### `llm/vector_store.py`
- `VectorStore`
  - Initializes SentenceTransformer `all-MiniLM-L6-v2`
  - Discovers or creates collection `crocodile` on Chroma REST API
- `get_relevant_context(query: str, n_results: int = 3) -> List[dict]`
- `format_context_for_prompt(contexts: List[dict]) -> str`

## Running locally
- With Docker Compose: see root `README.md` and `docker-compose.yaml`.
- Uvicorn (dev):
```bash
cd ai-service
uvicorn main:app --reload --port 3000
```

## Notes
- Ensure `chroma-db` is reachable at configured host/port.
- Requires network access to load `sentence-transformers` model on first start.
