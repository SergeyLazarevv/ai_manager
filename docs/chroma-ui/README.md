# chroma-ui Documentation

Streamlit application to explore ChromaDB collections and run simple queries.

## Running
- With Docker Compose (commented out in `docker-compose.yaml`); or run locally.

Local run:
```bash
cd chroma-ui
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

Environment:
- `CHROMA_HOST` (default `localhost`)
- `CHROMA_PORT` (default `8000`)

## Features
- Lists available collections
- Allows selecting a collection and running a similarity query
- Displays raw JSON results

## Example usage
- Start Chroma (`docker-compose up chroma-db`)
- Run Streamlit app as above
- Open http://localhost:8501 and query your collection
