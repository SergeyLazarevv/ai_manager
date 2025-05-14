import os
import json

class YandexGPTRequest:
    def __init__(self, question: str, context: str = None):
        self.model_uri = f"gpt://{os.getenv('YANDEX_CATALOG_ID')}/yandexgpt"
        self.completion_options = {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000",
            "reasoningOptions": {
                "mode": "DISABLED"
            }
        }
        self.messages = [
            {
                "role": "system",
                "text": question
            }
        ]
        
        if context:
            self.messages.append({
                "role": "user",
                "text": context
            })

    def to_dict(self):
        return {
            "modelUri": self.model_uri,
            "completionOptions": self.completion_options,
            "messages": self.messages
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
