from app.models.base_model import BaseModel
import openai

class GPT3Model(BaseModel):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate(self, context: str) -> str:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=context,
                max_tokens=200
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error al generar respuesta con GPT-3: {str(e)}"
