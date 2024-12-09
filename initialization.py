from sentence_transformers import SentenceTransformer
from app.services.query_service import QueryService
from app.services.pdf_service import PDFService
from app.models.ollama_model import OllamaModel

# Inicialización del cliente de embeddings
embedding_client = SentenceTransformer('all-MiniLM-L6-v2')

# Inicialización de los clientes de modelos generativos
ollama_client = OllamaModel(base_url="http://127.0.0.1:11434/api/generate")


# Diccionario de clientes de modelos
model_clients = {
    "embedding": embedding_client,
    "llama2": ollama_client,
    "llama3": ollama_client,
    "gemma": ollama_client,
}

# Inicialización del servicio de consultas
query_service = QueryService(
    index_path="app/faiss_indices/index.faiss",
    model_clients=model_clients
)

# Inicialización del servicio PDF
pdf_service = PDFService(
    temp_pdf_path="app/uploaded_pdfs",
    faiss_index_path="app/faiss_indices/index.faiss",
    query_service=query_service
)
