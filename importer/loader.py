import os
import time
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings

# Настройки из окружения
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")
CODE_DIR = os.getenv("CODE_DIR", "/code")

# Поддерживаемые расширения
SUPPORTED_EXTS = {".py", ".js", ".ts", ".php", ".java", ".go", ".rs", ".vue", ".tsx"}

def load_code_files():
    documents = []
    for root, _, files in os.walk(CODE_DIR):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTS):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        documents.append({
                            "content": content,
                            "metadata": {"source": path}
                        })
                except Exception as e:
                    print(f"Ошибка чтения {path}: {e}")
    return documents

def main():
    # Ждём, пока ChromaDB запустится
    time.sleep(5)

    # Загрузка кода
    # docs = load_code_files()
    # print(f"Загружено {len(docs)} файлов")

    # # Разделение на чанки
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=500,
    #     chunk_overlap=50,
    #     length_function=len
    # )

    # texts = []
    # metadatas = []
    # for doc in docs:
    #     chunks = text_splitter.split_text(doc["content"])
    #     texts.extend(chunks)
    #     metadatas.extend([{"source": doc["metadata"]["source"], "chunk": i} for i in range(len(chunks))])

    # # Подключение к ChromaDB через REST API
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Chroma(
    #     texts=texts,
    #     metadatas=metadatas,
    #     embedding=embeddings,
    #     persist_directory=f"http://{CHROMA_HOST}:{CHROMA_PORT}"
    # )

    # print("Данные успешно загружены в ChromaDB")

if __name__ == "__main__":
    main()