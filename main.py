from fastapi import FastAPI
from app.routes.pdf import router as pdf_router
from app.routes.query import router as query_router

# Crear instancia de FastAPI
app = FastAPI(
    title="Sistema de Consulta de Modelos y RAG",
    description="API para subir PDFs, procesarlos y consultar modelos generativos con FAISS y RAG",
    version="1.0.0"
)

# Registrar rutas
print("[DEBUG] main.py: Registrando rutas de PDF y Query.")
app.include_router(pdf_router, prefix="/pdf", tags=["PDF Processing"])
app.include_router(query_router, prefix="/query", tags=["Query Models"])
print("[DEBUG] main.py: Configuración completa.")
