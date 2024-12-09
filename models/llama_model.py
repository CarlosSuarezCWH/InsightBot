from app.models.base_model import BaseModel

class LLaMAModel(BaseModel):
    def __init__(self, model_path: str):
        self.model_path = model_path

    def generate(self, context: str) -> str:
        # Integración simulada. Reemplázalo con la llamada real a LLaMA.
        return f"LLaMA dice: {context}"
