# importer Documentation

FastAPI application and library to index files from a directory into ChromaDB using sentence-transformer embeddings.

## Base URL
- Local (Docker): `http://localhost:4000`

## API

### GET `/health`
Health check.

Response 200
```json
{"status": "ok"}
```

### POST `/imports`
Start indexing a directory into ChromaDB. Creates a collection named after the directory basename if it does not exist, then batches document additions.

Request body
```json
{
  "path": "/absolute/path/to/project"
}
```

Success response 200
```json
{"status": "success"}
```

cURL example
```bash
curl -X POST "http://localhost:4000/imports" \
  -H "Content-Type: application/json" \
  -d '{"path":"/home/sergey/projects/crocodile"}'
```

## Python client usage

```python
import requests

resp = requests.post(
    "http://localhost:4000/imports",
    json={"path": "/path/to/codebase"},
    timeout=300,
)
resp.raise_for_status()
print(resp.json())
```

## Library reference

### `schemas.py`
- `ImportRequest`:
  - Fields: `path: str`

### `loader.py`
- `should_index_file(file_path: str) -> bool`
  - Filters by extension and excluded directories
- `extract_language_info(file_path: str) -> dict`
  - Best-effort language detection from extension/config files
- `extract_info(file_path: str) -> dict`
  - Reads file, extracts normalized content and metadata for indexing
- `parse_directory(directory: str) -> None`
  - Encodes files with SentenceTransformer and adds to Chroma in batches

### `database/client.py`
- `ChromaClient`
  - `get_or_create_collection(name: str) -> str`
  - `add_documents(collection_id: str, documents: list, metadatas: list, embeddings: list)`

## Running locally
- With Docker Compose: see root `README.md` and `docker-compose.yaml`.
- Uvicorn (dev):
```bash
cd importer
uvicorn main:app --reload --port 4000
```

## Notes
- The first run downloads `all-MiniLM-L6-v2` model; needs internet access.
- Ensure `chroma-db` is reachable at configured host/port.
