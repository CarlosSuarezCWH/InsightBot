from app.models.base_model import BaseModel
import requests

class GPTNeoXModel(BaseModel):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def generate(self, context: str) -> str:
        try:
            response = requests.post(
                self.endpoint,
                json={"context": context}
            )
            return response.json().get("response", "Sin respuesta generada.")
        except Exception as e:
            return f"Error al generar respuesta con GPT-NeoX: {str(e)}"
