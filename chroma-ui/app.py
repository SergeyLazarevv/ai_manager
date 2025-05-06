import os
import streamlit as st
from chromadb import Client

# Конфигурация
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")

# Подключение к ChromaDB
client = Client(f"http://{CHROMA_HOST}:{CHROMA_PORT}")

# UI
st.set_page_config(page_title="ChromaDB Admin", layout="wide")
st.title("🔍 ChromaDB Admin UI")

# Показываем коллекции
collections = client.list_collections()
st.subheader("📦 Доступные коллекции")
st.write(collections)

# Поиск
st.subheader("🔎 Поиск в векторной БД")
query = st.text_input("Введите запрос")
if query:
    collection_name = st.selectbox("Выберите коллекцию", [c.name for c in collections])
    collection = client.get_collection(collection_name)
    
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    st.write("Результаты:")
    st.json(results)