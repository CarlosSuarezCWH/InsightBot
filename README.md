
# Sistema de Consulta de Modelos y RAG (Retrieval-Augmented Generation)

Este sistema es una API desarrollada con **FastAPI** para gestionar PDFs, procesarlos y consultar modelos generativos utilizando **FAISS** y técnicas de **RAG (Retrieval-Augmented Generation)**. Está diseñada para responder preguntas basándose en fragmentos relevantes de los documentos PDF cargados y enriquecidos con modelos de lenguaje natural.

---

## Funcionalidades Principales

### Procesamiento de PDFs
- Subida de archivos PDF.
- Indexación de contenido para consultas rápidas utilizando **FAISS**.
- Manejo de errores para asegurar que solo se procesen archivos válidos.

### Consultas a Modelos Generativos
- Recuperación de fragmentos relevantes basados en la pregunta del usuario.
- Generación de respuestas utilizando modelos como **LLaMA**, **GPT-NeoX**, o **SmolLM**.
- Soporte para múltiples idiomas, con traducción automática de preguntas y respuestas si es necesario.

---

## Cómo Funciona el RAG (Retrieval-Augmented Generation)

1. **Indexación del Contenido**:
   - Los documentos PDF cargados son procesados y transformados en fragmentos legibles.
   - Estos fragmentos se indexan en **FAISS**, una librería eficiente para búsquedas vectoriales.

2. **Consulta**:
   - Cuando el usuario realiza una pregunta, se busca en el índice para recuperar los fragmentos más relevantes.
   - Estos fragmentos proporcionan el contexto necesario para generar una respuesta precisa.

3. **Generación de Respuesta**:
   - Los fragmentos recuperados se combinan con la pregunta para formar un `prompt`.
   - Este `prompt` se pasa al modelo generativo seleccionado, que genera una respuesta basada en el contexto.

4. **Traducción**:
   - Si el idioma objetivo no coincide con el idioma del modelo, se realiza una traducción automática de entrada y salida.

### Flujo Técnico del RAG
1. **Carga y Procesamiento del PDF**:
   - Extraer texto y dividirlo en fragmentos.
   - Convertir los fragmentos en representaciones vectoriales con un modelo de embeddings.
   - Guardar los vectores en el índice FAISS.

2. **Consulta y Respuesta**:
   - Convertir la pregunta del usuario en un vector utilizando el mismo modelo de embeddings.
   - Recuperar los fragmentos más cercanos en el espacio vectorial.
   - Combinar la pregunta y los fragmentos recuperados en un `prompt`.
   - Pasar el `prompt` al modelo generativo para producir una respuesta.

---

## Requisitos Previos

1. **Python 3.9 o superior**.
2. Servidor con:
   - **50 GB de RAM**.
   - **8 CPUs**.
3. Espacio de almacenamiento para indexar y almacenar PDFs.
4. Opcional: GPU para mejorar el rendimiento de modelos.

---

## Instalación

### Clonar el Repositorio
```bash
git clone https://github.com/CarlosSuarezCWH/InsightBot.git
cd InsightBot
```

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Configurar Variables de Entorno
Crea un archivo `.env` en el directorio raíz y define las siguientes variables:
```env
TEMP_PDF_PATH=./temp_pdfs
INDEX_PATH=./index.faiss
```

---

## Uso

### Ejecutar el Servidor
Para ejecutar el servidor, utiliza el siguiente comando:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Esto inicia el servidor en `http://0.0.0.0:8000`.

### Documentación Interactiva
Accede a la documentación en:
- **Swagger UI**: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)
- **ReDoc**: [http://0.0.0.0:8000/redoc](http://0.0.0.0:8000/redoc)

---

## Endpoints

### `/pdf/upload` (POST)
**Descripción**: Subir un archivo PDF para procesarlo y añadirlo al índice.

**Parámetros**:
- `file` (archivo): El archivo PDF a subir.

**Respuesta**:
```json
{
  "message": "PDF procesado y añadido al índice con éxito."
}
```

**Ejemplo**:
```bash
curl -X POST "http://0.0.0.0:8000/pdf/upload"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"   -F "file=@example.pdf"
```

---

### `/query` (POST)
**Descripción**: Realiza una consulta a los documentos indexados y genera una respuesta utilizando un modelo generativo.

**Parámetros**:
- `question` (str): La pregunta del usuario.
- `target_language` (str): Idioma deseado para la respuesta (por defecto, "es").
- `model_name` (str): Nombre del modelo a utilizar (por defecto, "llama2").

**Respuesta**:
```json
{
  "question": "¿Qué evento desató el conflicto?",
  "answer": "El evento fue la apertura de la Puerta a Jahannam.",
  "model": "llama2",
  "retrieved_fragments": [
    "Fragmento 1...",
    "Fragmento 2...",
    "Fragmento 3..."
  ]
}
```

**Ejemplo**:
```bash
curl -X POST "http://0.0.0.0:8000/query"   -H "accept: application/json"   -H "Content-Type: application/json"   -d '{
    "question": "¿Qué evento desató el conflicto?",
    "target_language": "es",
    "model_name": "llama3"
  }'
```

---

## Mejora del Rendimiento

### Escalabilidad
- Usa el parámetro `--workers` en `uvicorn` para paralelizar las peticiones:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
  ```

### Optimización de Modelos
- Utiliza **SmolLM** o modelos ligeros en servidores con recursos limitados.
- Si tienes GPU, instala PyTorch con soporte CUDA.

---

## Desarrollo Futuro

1. **Soporte para otros formatos**: Añadir soporte para Word, TXT, y más.
2. **Autenticación**: Implementar autenticación para proteger el acceso a los endpoints.
3. **Mejoras en la interfaz**: Crear una interfaz gráfica para gestionar PDFs y consultas.

---

## Licencia

Este proyecto está bajo la **Licencia MIT**. Puedes usarlo, modificarlo y distribuirlo libremente, siempre y cuando menciones al autor original.
