# Project Documentation

## Overview
This repository contains multiple services that provide an AI query API backed by ChromaDB and a content importer for building the knowledge base. This documentation covers all public APIs, functions, and components, with examples and usage instructions.

- ai-service: FastAPI application that exposes query endpoints and integrates with YandexGPT plus ChromaDB context.
- importer: FastAPI application and library for indexing files into ChromaDB.
- chroma-ui: Streamlit UI for exploring ChromaDB (optional).

## Quickstart

### Prerequisites
- Docker and Docker Compose installed
- Internet access to download models and images

### Start the stack
```bash
docker-compose up --build --remove-orphans
```

### Services
- ai-service API: http://localhost:3000/docs
- importer API: http://localhost:4000/docs
- chroma-db HTTP API: http://localhost:8000

## Repository structure

```
ai-service/
  api/routes.py
  llm/{base.py, client.py, vector_store.py}
  config/settings.py
  schemas.py
  main.py
importer/
  api/routes.py
  database/client.py
  loader.py
  schemas.py
  main.py
chroma-ui/
  app.py
```

## Next steps
- See `docs/ai-service/README.md` for API and client reference
- See `docs/importer/README.md` for API and library reference
- See `docs/chroma-ui/README.md` for UI usage
