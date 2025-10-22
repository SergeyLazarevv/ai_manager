# chroma bootstrap

Helper script to pre-create common collections in Chroma REST server.

## File
- `chroma/init_collections.py`

## Environment
- `CHROMA_HOST` (default `chroma-db2` in script; override via env)
- `CHROMA_PORT` (default `8000`)
- `CHROMA_TENANT` (default `default_tenant`)
- `CHROMA_DATABASE` (default `default_database`)

## Behavior
- Waits for Chroma to be ready
- Ensures collections exist: `code_projects`, `documentation`, `logs` (dimension 384)
- Uses cosine distance and records model name in metadata

## Run inside Docker Compose
The service `chroma-init` is defined in `docker-compose.yaml` and depends on `chroma-db`.

Enable its entrypoint to run automatically after Chroma starts (uncomment if needed).

## Manual run
```bash
python chroma/init_collections.py
```
