from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def generate(self, context: str) -> str:
        """Genera una respuesta basada en el contexto proporcionado."""
        pass
