# InsightBot
Un servicio basado en inteligencia artificial para consultar documentos PDF, generando respuestas precisas mediante fragmentos relevantes y modelos generativos como Llama.


**Características**

 - Procesamiento de PDFs: Subida, procesamiento y extracción de contenido de archivos PDF.     
 - Consultas a Modelos Generativos: Soporte para múltiples modelos como LLaMA, GPT-NeoX y SmolLM.    
- Integración RAG: Utiliza FAISS para mejorar la recuperación de fragmentos relevantes antes de generar respuestas.     
- API Documentada: Documentación interactiva en /redoc y /docs.

**Requisitos Previos**
Antes de instalar y ejecutar el proyecto, asegúrate de tener instalado:

 - Python 3.9 o superior.
 - Pipenv o cualquier herramienta para manejar entornos virtuales.
 - Un servidor configurado para modelos como Ollama.

**Instalación**
Clona este repositorio:

    git clone https://github.com/CarlosSuarezCWH/InsightBot.git
    cd InsightBot

**Crea un entorno virtual:**

    python -m venv venv
    source venv/bin/activate

 En Windows usa `venv\Scripts\activate`


**Instala las dependencias:**

    pip install -r requirements.txt



**Configura las variables de entorno:** 
Crea un archivo .env y añade las siguientes configuraciones:

    TEMP_PDF_PATH=./temp_pdfs
    MODEL_SERVER_URL=http://localhost:11434

**Inicia el servidor:**
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

**Uso**

Endpoints Principales
Subir PDFs: POST /pdf/upload
Sube un archivo PDF y lo procesa para indexarlo.

Hacer consultas: POST /query
Consulta información basada en los fragmentos relevantes del índice y modelos generativos.

**Ejemplo de Consulta**

    curl -X 'POST' \
      'http://localhost:8000/query/?question=¿Qué contiene el documento?&target_language=es&model_name=llama2' \
      -H 'accept: application/json' \
      -d ''


**Créditos**
Desarrollado por Carlos Mancera and Global Crew.
Inspirado por tecnologías avanzadas de IA como Ollama, FastAPI y FAISS.


