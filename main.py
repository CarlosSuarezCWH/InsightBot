from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.pdf import router as pdf_router
from app.routes.query import router as query_router

# Crear instancia de FastAPI
app = FastAPI(
    title="Sistema de Consulta de Modelos y RAG",
    description="API para subir PDFs, procesarlos y consultar modelos generativos con FAISS y RAG",
    version="1.0.0"
)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por una lista específica de dominios en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

# Registrar rutas
print("[DEBUG] main.py: Registrando rutas de PDF y Query.")
app.include_router(pdf_router, prefix="/pdf", tags=["PDF Processing"])
app.include_router(query_router, prefix="/query", tags=["Query Models"])
print("[DEBUG] main.py: Configuración completa.")
