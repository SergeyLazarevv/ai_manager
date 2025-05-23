import os
import re
from sentence_transformers import SentenceTransformer
from database.client import ChromaClient

# Конфигурация
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def parse_directory(directory: str):
    client = ChromaClient()
    collection_name = os.path.basename(os.path.normpath(directory))
    collection_id = client.get_or_create_collection(collection_name)
    
    print(f"Обрабатываем директорию: {directory}")
    
    documents = []
    metadatas = []
    embeddings = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            # if not file.endswith(".php"):
            #     continue
            
            file_path = os.path.join(root, file)
            try:
                data = extract_info(file_path)
                print(f"Обрабатываем файл: {file_path}")
                if not data["text"]:
                    continue
                
                # Формируем батч для отправки
                documents.append(data["text"])
                metadatas.append(data["metadata"])
                embeddings.append(model.encode(data["text"]).tolist())
                
                # Отправляем батчи по 100 документов
                if len(documents) >= 100:
                    client.add_documents(collection_id, documents, metadatas, embeddings)
                    documents.clear()
                    metadatas.clear()
                    embeddings.clear()
                    
            except Exception as e:
                print(f"Ошибка в файле {file_path}: {str(e)}")
    
    # Отправляем оставшиеся документы
    if documents:
        client.add_documents(collection_id, documents, metadatas, embeddings)

def extract_info(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 6. Улучшенные регулярные выражения для парсинга
        comment_match = re.search(
            r'/\*\*(.*?)\*/', 
            content, 
            re.DOTALL
        )
        
        class_match = re.search(
            r'class\s+([a-zA-Z0-9_]+)\s*{', 
            content
        )

        comment = comment_match.group(1).strip() if comment_match else ""
        class_name = class_match.group(1) if class_match else os.path.basename(file_path)

        # 7. Ограничение длины контента и очистка текста
        content_sample = re.sub(r'\s+', ' ', content[:2000]).strip()

        return {
            "text": f"{content_sample}",
            "metadata": {
                "service_name": os.path.basename(os.path.dirname(file_path)),
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
                "class_name": class_name
            }
        }
    except Exception as e:
        print(f"Ошибка чтения файла {file_path}: {str(e)}")
        return {"text": "", "metadata": {}}

