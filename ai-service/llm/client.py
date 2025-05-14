from config.settings import Settings
from llm.base import BaseLLMClient
import httpx
from dotenv import find_dotenv
import os
from functools import lru_cache
from dto.yandex_llm_request import YandexGPTRequest   

class Client(BaseLLMClient):
    def __init__(self, settings: Settings):
        self.url = settings.YANDEX_LLM_URL
        self.token = 't1.9euelZrLmMyZypaRzImKl4-YxsmTju3rnpWaysialcbJyozLmJ3JmIqVmJLl8_cPB2w--e8SUk9Q_d3z9081aT757xJST1D9zef1656VmpbKkJnHiZ6RyJmTkM-Wz5WJ7_zF656VmpbKkJnHiZ6RyJmTkM-Wz5WJ.nB4y2R9TSB0x1xCbwusGlMCsHWTFKx4HBRP7qHc28OqLuHSgGCK4BeP33OK4z79kisRsjnWHXjT4nSS9OJ5LDQ'

    def query(self, prompt: str) -> str:
        print('in query method')
        request_data = YandexGPTRequest(prompt).to_dict()
        print('request_data', request_data)

        response = httpx.post(
            url=self.url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"  # Явно указываем Content-Type
            },
            json={
                **request_data,  # Распаковываем данные из запроса
                "max_tokens": 2000
            },
            timeout=60.0
        )
        response.raise_for_status()
        response = response.json()
        # print(response)
        # print(response.json())
        # print('----------')
        # print(response.json()['result'])
        # print(response.json().result)
        # print('--------------')
        # print(response.json().result.alternatives[0].message.text)

        # return response.json()['result']['alternatives'][0]['message']['text']
        return {
            "body": response['result']['alternatives'][0]['message']['text'],
            "model_version": response['result']['modelVersion'],
            "input_text_tokens": response['result']['usage']['inputTextTokens'],
            "completion_tokens": response['result']['usage']['completionTokens'],
            "total_tokens": response['result']['usage']['totalTokens'],
        } 
        

# def get_llm_client(provider: str, settings: Settings) -> BaseLLMClient:
#     print(12121212)
#     print(provider)
#     print(3434343434)
#     print(os.getenv("LLM_PROVIDER"))
#     if provider == "yandex":
#         return Client(settings)
#     raise ValueError(f"Unknown LLM provider: {provider}")