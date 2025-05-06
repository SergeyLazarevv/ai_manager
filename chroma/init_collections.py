import requests
import os
import time
from dotenv import load_dotenv

# === Настройки из окружения ===
load_dotenv()
CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma-db2")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")
CHROMA_TENANT = os.getenv("CHROMA_TENANT", "default_tenant")
CHROMA_DATABASE = os.getenv("CHROMA_DATABASE", "default_database")
print(CHROMA_HOST)

# === Коллекции и их параметры ===
COLLECTIONS = {
    "code_projects": {"dimension": 384, "model": "all-MiniLM-L6-v2"},
    "documentation": {"dimension": 384, "model": "all-MiniLM-L6-v2"},
    "logs": {"dimension": 384, "model": "all-MiniLM-L6-v2"},
}

# === Базовый URL API ===
BASE_URL = f"http://{CHROMA_HOST}:{CHROMA_PORT}/api/v1"

def wait_for_chroma():
    """Ждём, пока сервер станет доступным"""
    for i in range(15):
        try:
            response = requests.get(f"{BASE_URL}/tenants/{CHROMA_TENANT}", timeout=5)
            if response.status_code == 200:
                print("[OK] Сервер Chroma доступен")
                return True
        except requests.exceptions.RequestException:
            print(f"[WAIT] Сервер не доступен, попытка {i+1}/15...")
            time.sleep(3)
    raise Exception("Сервер Chroma не запустился за отведённое время")

def collection_exists(name: str) -> bool:
    """Проверяет существование коллекции через API"""
    url = f"{BASE_URL}/collections/{name}"
    params = {
        "tenant": CHROMA_TENANT,
        "database": CHROMA_DATABASE
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        
        # Коллекция существует
        if response.status_code == 200:
            print(f"[OK] Коллекция '{name}' уже существует")
            return True
            
        # Сервер возвращает 500, если коллекция не существует
        if response.status_code == 500:
            error_text = response.json().get("error", "")
            if "does not exist" in error_text:
                print(f"[-] Коллекция '{name}' не найдена, будет создана")
                return False
                
        # Неожиданный ответ
        print(f"[ERROR] Неожиданный ответ от сервера при проверке коллекции '{name}'")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")  # Обрезаем длинные ответы
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Ошибка сети при проверке коллекции '{name}': {e}")
        return False

def create_collection(name: str, dimension: int, model: str):
    """Создаёт коллекцию через API"""
    url = f"{BASE_URL}/collections"
    params = {
        "tenant": CHROMA_TENANT,
        "database": CHROMA_DATABASE
    }
    payload = {
        "name": name,
        "metadata": {
            "hnsw:space": "cosine",
            "model": model
        },
        "dimension": dimension
    }

    try:
        response = requests.post(url, params=params, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"[+] Коллекция '{name}' успешно создана")
            return True
            
        if response.status_code == 500:
            error_text = response.json().get("error", "")
            if "UniqueConstraintError" in error_text:
                print(f"[OK] Коллекция '{name}' уже существует (через UniqueConstraintError)")
                return True
            elif "does not exist" in error_text:
                print(f"[ERROR] Не удалось создать коллекцию '{name}': сервер сообщает, что она не существует")
                return False
                
        print(f"[ERROR] Не удалось создать коллекцию '{name}'")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Сеть: не удалось создать коллекцию '{name}': {e}")
        return False

def create_collections():
    """Основная функция создания коллекций"""
    for name, config in COLLECTIONS.items():
        if not collection_exists(name):
            success = create_collection(name, config["dimension"], config["model"])
            if success:
                print(f"[+] Коллекция '{name}' успешно обработана")
            else:
                print(f"[ERROR] Коллекция '{name}' не создана")

if __name__ == "__main__":
    if wait_for_chroma():
        create_collections()
    else:
        print("[ERROR] Сервер не запустился")