from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    def query(self, prompt: str) -> str:
        pass
