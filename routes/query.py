from fastapi import APIRouter
from app.initialization import query_service
from app.utils.translation import Translator

router = APIRouter()
translator = Translator()

def filter_relevant_fragments(question, fragments):
    keywords = question.lower().split()  # Palabras clave de la pregunta
    relevant_fragments = [frag for frag in fragments if any(kw in frag.lower() for kw in keywords)]
    return relevant_fragments if relevant_fragments else fragments[:3]  # Usa los primeros 3 si no hay coincidencias


@router.post("/")
async def query_pdf(question: str, target_language: str = "es", model_name: str = "llama2"):
    print(f"[DEBUG] query_pdf: Procesando con modelo {model_name}.")

    # Traducir la pregunta al inglés si es necesario
    question_in_english = translator.to_english(question)

    # Consultar el índice FAISS
    distances, indices = query_service.query(question_in_english)
    fragments = query_service.get_fragments(indices, target_language, distances)

    if not fragments:
        return {
            "question": question,
            "answer": "No se encontraron fragmentos relevantes en el texto proporcionado.",
            "model": model_name,
            "retrieved_fragments": []
        }

    # Filtrar los fragmentos relevantes
    relevant_fragments = filter_relevant_fragments(question, fragments)

    # Generar la respuesta
    try:
        answer = query_service.generate_response(relevant_fragments, question, model_name)
        if not answer.strip():  # Manejo explícito de respuesta vacía
            answer = "No se pudo generar una respuesta relevante a partir del contexto proporcionado."
    except Exception as e:
        answer = f"Error al generar la respuesta: {str(e)}"

    return {
        "question": question,
        "answer": answer.strip(),
        "model": model_name,
        "retrieved_fragments": fragments
    }

