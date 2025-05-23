import os
import re
import json
from sentence_transformers import SentenceTransformer
from database.client import ChromaClient

# Конфигурация
MODEL_NAME = "all-MiniLM-L6-v2"

# Расширения файлов для индексации
INCLUDE_EXTENSIONS = {
    # Исходный код
    '.py', '.js', '.ts', '.php', '.go', '.rb', '.java', '.cpp', '.c', '.h', '.hpp',
    # Конфигурационные файлы
    '.json', '.yaml', '.yml', '.toml', '.ini', '.env.example',
    # Документация
    '.md', '.rst', '.txt',
    # Веб
    '.html', '.css', '.scss', '.sass',
    # Шаблоны
    '.template', '.tmpl', '.j2'
}

# Директории для исключения
EXCLUDE_DIRS = {
    '.git', '.svn', '.hg',  # Системы контроля версий
    'node_modules', 'vendor', 'venv', '.venv', 'env',  # Зависимости
    '__pycache__', '.pytest_cache', '.coverage',  # Кэш Python
    'dist', 'build', 'target',  # Сборки
    '.idea', '.vscode',  # IDE
    'tmp', 'temp', 'logs'  # Временные файлы
}

# Конфигурационные файлы для специальной обработки
CONFIG_FILES = {
    'package.json': 'JavaScript/Node.js',
    'composer.json': 'PHP',
    'requirements.txt': 'Python',
    'go.mod': 'Go',
    'Gemfile': 'Ruby',
    'pom.xml': 'Java',
    'build.gradle': 'Java',
    'Cargo.toml': 'Rust',
    'mix.exs': 'Elixir',
    'pubspec.yaml': 'Dart/Flutter'
}

model = SentenceTransformer(MODEL_NAME)

def should_index_file(file_path: str) -> bool:
    """Проверяет, нужно ли индексировать файл"""
    # Проверяем расширение
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in INCLUDE_EXTENSIONS:
        return False
        
    # Проверяем, не находится ли файл в исключенной директории
    parts = os.path.normpath(file_path).split(os.sep)
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False
            
    return True

def extract_language_info(file_path: str) -> dict:
    """Извлекает информацию о языке программирования из файла"""
    file_name = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    
    # Проверяем конфигурационные файлы
    if file_name in CONFIG_FILES:
        return {"language": CONFIG_FILES[file_name]}
        
    # Определяем язык по расширению
    ext_to_lang = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.php': 'PHP',
        '.go': 'Go',
        '.rb': 'Ruby',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C/C++ Header',
        '.hpp': 'C++ Header',
        '.rs': 'Rust',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.elixir': 'Elixir',
        '.ex': 'Elixir',
        '.dart': 'Dart',
        '.tsx': 'TypeScript React',
        '.jsx': 'JavaScript React'
    }
    
    return {"language": ext_to_lang.get(ext, "Unknown")}

def extract_info(file_path: str) -> dict:
    """Извлекает информацию из файла"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Получаем базовую информацию о файле
        file_name = os.path.basename(file_path)
        language_info = extract_language_info(file_path)
        
        # Для конфигурационных файлов пытаемся извлечь дополнительную информацию
        if file_name in CONFIG_FILES:
            try:
                config_data = json.loads(content)
                if file_name == 'package.json':
                    content = f"Project: {config_data.get('name', 'Unknown')}\n"
                    content += f"Description: {config_data.get('description', '')}\n"
                    content += f"Dependencies: {json.dumps(config_data.get('dependencies', {}), indent=2)}\n"
                elif file_name == 'composer.json':
                    content = f"Project: {config_data.get('name', 'Unknown')}\n"
                    content += f"Description: {config_data.get('description', '')}\n"
                    content += f"Require: {json.dumps(config_data.get('require', {}), indent=2)}\n"
            except json.JSONDecodeError:
                pass

        # Извлекаем комментарии и классы
        comment_match = re.search(r'/\*\*(.*?)\*/', content, re.DOTALL)
        class_match = re.search(r'class\s+([a-zA-Z0-9_]+)\s*{', content)
        
        comment = comment_match.group(1).strip() if comment_match else ""
        class_name = class_match.group(1) if class_match else os.path.basename(file_path)
        
        # Ограничиваем длину контента и очищаем текст
        content_sample = re.sub(r'\s+', ' ', content[:2000]).strip()
        
        # Формируем текст для индексации
        indexed_text = f"Language: {language_info['language']}\n"
        if comment:
            indexed_text += f"Documentation: {comment}\n"
        indexed_text += f"Content: {content_sample}"

        return {
            "text": indexed_text,
            "metadata": {
                "service_name": os.path.basename(os.path.dirname(file_path)),
                "file_path": file_path,
                "file_name": file_name,
                "class_name": class_name,
                "language": language_info['language']
            }
        }
    except Exception as e:
        print(f"Ошибка чтения файла {file_path}: {str(e)}")
        return {"text": "", "metadata": {}}

def parse_directory(directory: str):
    """Обрабатывает директорию и индексирует файлы"""
    client = ChromaClient()
    collection_name = os.path.basename(os.path.normpath(directory))
    collection_id = client.get_or_create_collection(collection_name)
    
    print(f"Обрабатываем директорию: {directory}")
    
    documents = []
    metadatas = []
    embeddings = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            if not should_index_file(file_path):
                continue
                
            try:
                data = extract_info(file_path)
                if not data["text"]:
                    continue
                    
                print(f"Обрабатываем файл: {file_path}")
                
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

