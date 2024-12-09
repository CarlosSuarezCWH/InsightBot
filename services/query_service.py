from typing import List, Tuple
import numpy as np
import faiss
import os
from app.models.ollama_model import OllamaModel
from app.models.gpt_neox_model import GPTNeoXModel
from app.models.llama_model import LLaMAModel


class QueryService:
    def __init__(self, index_path: str, model_clients: dict, fragments: list = None, translator=None):
        """
        Inicializa el servicio de consultas con FAISS y clientes de modelos.

        :param index_path: Ruta al índice FAISS.
        :param model_clients: Diccionario con clientes para modelos generativos.
        :param fragments: Lista de fragmentos pre-cargados (opcional).
        :param translator: Servicio de traducción (opcional).
        """
        self.index_path = index_path
        self.translator = translator

        # Cargar o crear el índice FAISS
        if os.path.exists(index_path):
            try:
                self.index = faiss.read_index(index_path)
                print(f"[DEBUG] Índice cargado desde {index_path} con {self.index.ntotal} vectores.")
            except Exception as e:
                print(f"[ERROR] No se pudo cargar el índice desde {index_path}: {e}")
                self._create_new_index()
        else:
            print(f"[INFO] No se encontró el índice en {index_path}. Creando un nuevo índice.")
            self._create_new_index()

        self.model_clients = model_clients
        self.fragments = fragments or []
        print(f"[DEBUG] QueryService inicializado con modelos: {list(model_clients.keys())}")

        # Validar sincronización entre índice y fragmentos
        self.validate_and_sync_index()

    def _create_new_index(self):
        """
        Crea un nuevo índice FAISS.
        """
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        self.index = faiss.IndexFlatL2(384)  # Dimensión del embedding debe ser 384
        faiss.write_index(self.index, self.index_path)
        print(f"[INFO] Nuevo índice FAISS creado y guardado en {self.index_path}.")

    def validate_and_sync_index(self):
        """
        Valida si el índice FAISS y los fragmentos están sincronizados.
        """
        print(f"[DEBUG] Fragmentos disponibles antes de la sincronización: {len(self.fragments)}")

        if not self.fragments:
            print("[ERROR] No hay fragmentos disponibles para sincronizar con el índice FAISS.")
            return

        if len(self.fragments) != self.index.ntotal:
            print(f"[WARNING] Desajuste: {len(self.fragments)} fragmentos, {self.index.ntotal} vectores en índice.")
            print("[INFO] Reseteando índice y sincronizando con los fragmentos...")
            try:
                self.index.reset()
                embeddings = self.model_clients["embedding"].encode(self.fragments, convert_to_tensor=False)
                self.add_to_index(np.array(embeddings), self.fragments)
                print("[INFO] Índice sincronizado correctamente.")
            except Exception as e:
                print(f"[ERROR] Fallo al sincronizar el índice: {e}")
        else:
            print("[INFO] El índice FAISS y los fragmentos están sincronizados.")

    def query(self, question: str, k: int = 10, distance_threshold: float = 1.7) -> Tuple[np.ndarray, np.ndarray]:
        """
        Realiza una consulta al índice FAISS.

        :param question: Pregunta del usuario.
        :param k: Número de fragmentos similares a recuperar.
        :param distance_threshold: Umbral de distancia para filtrar resultados irrelevantes.
        :return: Distancias e índices de los fragmentos más similares.
        """
        question_embedding = self.model_clients["embedding"].encode([question])
        distances, indices = self.index.search(np.array(question_embedding, dtype=np.float32), k)

        # Filtrar resultados por distancia
        valid_indices = [
            indices[0][i] for i in range(len(distances[0])) if distances[0][i] < distance_threshold
        ]
        valid_distances = [d for d in distances[0] if d < distance_threshold]

        if not valid_indices:
            print("[WARNING] No se encontraron fragmentos relevantes. Retornando los más cercanos sin filtrar.")
            valid_indices = indices[0]
            valid_distances = distances[0]

        print(f"[DEBUG] Distancias originales: {distances}")
        print(f"[DEBUG] Índices originales: {indices}")
        print(f"[DEBUG] Distancias válidas: {valid_distances}")
        print(f"[DEBUG] Índices válidos: {valid_indices}")

        return np.array(valid_distances), np.array(valid_indices)

    def get_fragments(self, indices: List[int], target_language: str = "es", distances: List[float] = None) -> List[str]:
        """
        Recupera los fragmentos correspondientes a los índices dados y los traduce al idioma deseado.

        :param indices: Lista de índices de los fragmentos a recuperar.
        :param target_language: Idioma deseado para los fragmentos.
        :param distances: Distancias asociadas a los índices (opcional).
        :return: Lista de fragmentos traducidos.
        """
        if isinstance(indices, np.ndarray):
            indices = indices.tolist()

        distances = distances if distances is not None and len(distances) > 0 else []

        result_fragments = []
        for idx, distance in zip(indices, distances):
            if 0 <= idx < len(self.fragments):
                fragment = self.fragments[idx]
                print(f"[DEBUG] Fragmento recuperado (índice {idx}, distancia {distance}): {fragment[:200]}...")
                if self.translator and target_language != "en":
                    try:
                        fragment = self.translator.to_target(fragment, target_language)
                    except Exception as e:
                        print(f"[WARNING] Error al traducir fragmento: {e}")
                result_fragments.append(fragment)
            else:
                print(f"[WARNING] Índice {idx} fuera del rango válido.")
        
        return result_fragments


    def generate_response(self, fragments: List[str], question: str, model_name: str, target_language: str = "es") -> str:
        """
        Genera una respuesta utilizando fragmentos recuperados y un modelo generativo.

        :param fragments: Lista de fragmentos relevantes.
        :param question: Pregunta del usuario.
        :param model_name: Nombre del modelo generativo a utilizar.
        :param target_language: Idioma deseado para la respuesta.
        :return: Respuesta generada en el idioma deseado.
        """
        if not fragments:
            return "No se encontraron fragmentos relevantes para esta pregunta."

        try:
            # Crear contexto con los fragmentos relevantes
            context = "\n".join(fragments[:5])

            # Construir el prompt
            prompt = (
                f"Contexto del juego:\n{context}\n\n"
                f"Pregunta: {question}\n\n"
                "Instrucciones: Responde con información específica basada en el contexto proporcionado. "
                "Si el contexto no tiene información suficiente, menciona que falta información clara, pero intenta responder lo mejor posible en español."
            )

            print(f"[DEBUG] Prompt enviado al modelo:\n{prompt}")

            # Verificar si el modelo está disponible
            model_client = self.model_clients.get(model_name)
            if not model_client:
                return f"[ERROR] El modelo '{model_name}' no está disponible."

            # Generar respuesta usando el cliente del modelo
            if isinstance(model_client, OllamaModel):
                response = model_client.generate(prompt=prompt, model_name=model_name)
            else:
                response = model_client.generate(prompt=prompt)

            print(f"[DEBUG] Respuesta bruta del modelo:\n{response}")

            # Capturar y procesar la respuesta generada
            if response and isinstance(response, str):
                # Si la respuesta contiene contenido válido, la devolvemos directamente
                return response.strip()

            # Fallback si no se genera una respuesta válida
            return "No se pudo generar una respuesta relevante a partir del contexto proporcionado."

        except Exception as e:
            print(f"[ERROR] Error al generar la respuesta: {e}")
            return "Ocurrió un error al intentar generar la respuesta."






    def extract_keywords_from_question(self, question: str) -> List[str]:
        """
        Extrae palabras clave de una pregunta utilizando heurísticas simples.

        :param question: Pregunta del usuario.
        :return: Lista de palabras clave.
        """
        # Convertir en minúsculas y eliminar puntuaciones simples
        question = question.lower().replace("¿", "").replace("?", "").strip()
        stop_words = {"qué", "cuál", "cuáles", "cómo", "cuándo", "dónde", "por", "qué", "es", "la", "el", "los", "las", "de", "un", "una", "para", "y"}
        keywords = [word for word in question.split() if word not in stop_words]
        return keywords




    def add_to_index(self, embeddings: np.ndarray, fragments: List[str]):
        """
        Añade embeddings y fragmentos al índice FAISS.

        :param embeddings: Embeddings generados.
        :param fragments: Fragmentos correspondientes.
        """
        if embeddings is None or len(embeddings) == 0:
            raise ValueError("[ERROR] Los embeddings están vacíos. No se pueden agregar al índice FAISS.")
        if len(embeddings) != len(fragments):
            raise ValueError("[ERROR] La cantidad de embeddings no coincide con la cantidad de fragmentos.")

        self.index.add(embeddings)
        self.fragments = fragments
        faiss.write_index(self.index, self.index_path)
        print(f"[INFO] Añadidos {len(embeddings)} embeddings al índice.")

    def inspect_index(self):
        """
        Inspecciona el estado del índice FAISS.
        """
        if not hasattr(self, "index") or self.index is None:
            print("[ERROR] Índice FAISS no inicializado.")
        else:
            print(f"[INFO] El índice FAISS contiene {self.index.ntotal} vectores.")

    def test_query(self, query: str, k: int = 5):
        """
        Realiza una prueba directa al índice FAISS con una consulta específica.
        """
        question_embedding = self.model_clients["embedding"].encode([query])
        distances, indices = self.index.search(np.array(question_embedding, dtype=np.float32), k)
        print(f"[DEBUG] Distancias: {distances}")
        print(f"[DEBUG] Índices: {indices}")

        for idx in indices[0]:
            if idx < len(self.fragments):
                print(f"[DEBUG] Fragmento devuelto (índice {idx}): {self.fragments[idx][:200]}...")
