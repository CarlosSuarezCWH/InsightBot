import os

class Config:
    # Rutas de archivos y directorios
    TEMP_PDF_PATH = os.getenv("TEMP_PDF_PATH", "app/uploaded_pdfs")  # Directorio temporal para PDFs subidos
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "app/faiss_indices/index.faiss")  # Ruta del índice FAISS

    # Configuración de los modelos
    MODEL_CONFIGS = {
        "llama2": {
            "name": "llama2",
            "endpoint": "http://127.0.0.1:11434/api/generate",
            "model": "llama2",
        },
        "mistral": {
            "name": "mistral",
            "endpoint": "http://127.0.0.1:11434/api/generate",
            "model": "mistral",
        },
        "gemma": {
            "name": "gemma",
            "endpoint": "http://127.0.0.1:11434/api/generate",
            "model": "gemma",
        },
    }

    # Configuración de FAISS y embeddings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Modelo para generar embeddings

    # Variables de entorno adicionales
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
