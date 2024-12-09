import requests
import json

class OllamaModel:
    def __init__(self, base_url: str = "http://127.0.0.1:11434/api/generate"):
        """
        Inicializa el cliente del modelo Ollama.

        :param base_url: URL base del servidor Ollama.
        """
        self.base_url = base_url

    def generate(self, prompt: str, model_name: str) -> str:
        """
        Genera una respuesta usando un modelo Ollama.

        :param prompt: Prompt para el modelo.
        :param model_name: Nombre del modelo.
        :return: Respuesta generada por el modelo.
        """
        
        payload = {"prompt": prompt, "model": model_name}
        try:
            response = requests.post(self.base_url, json=payload, timeout=3000, stream=True)
            response.raise_for_status()

            result = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            result += data["response"]
                        if data.get("done"):
                            break  # Salir del bucle cuando la respuesta esté completa
                    except json.JSONDecodeError as e:
                        print(f"[WARNING] OllamaModel: No se pudo decodificar una línea de la respuesta: {line}")
                        continue
            return result.strip()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] OllamaModel: Error al comunicarse con el modelo '{model_name}': {e}")
            return f"Error: {e}"
