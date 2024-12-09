from app.models.ollama_model import OllamaModel
from app.models.gpt3_model import GPT3Model
from app.models.gpt_neox_model import GPTNeoXModel
from app.models.llama_model import LLaMAModel

class ModelFactory:
    @staticmethod
    def get_model(model_name: str, config: dict):
        if model_name == "ollama":
            return OllamaModel(config.get("model_path", ""))
        elif model_name == "gpt3":
            return GPT3Model(config.get("api_key", ""))
        elif model_name == "gpt_neox":
            return GPTNeoXModel(config.get("endpoint", ""))
        elif model_name == "llama":
            return LLaMAModel(config.get("model_path", ""))
        else:
            raise ValueError(f"Modelo desconocido: {model_name}")
