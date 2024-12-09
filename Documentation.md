
# Sistema de Consulta de Modelos y RAG

Este proyecto proporciona una API basada en **FastAPI** para procesar archivos PDF, extraer información, indexarla utilizando **FAISS**, y realizar consultas utilizando **modelos generativos** como `llama2`, `SmolLM` y otros.

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Descripción de Archivos](#descripción-de-archivos)
- [Cómo Funciona](#cómo-funciona)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)

---

## Estructura del Proyecto

```plaintext
app/
├── config.py
├── initialization.py
├── main.py
├── models/
│   ├── ollama_model.py
├── routes/
│   ├── pdf.py
│   ├── query.py
├── services/
│   ├── pdf_service.py
│   ├── query_service.py
├── utils/
│   ├── translation.py
│   ├── faiss_index.py
README.md
requirements.txt
```

---

## Descripción de Archivos

### **app/config.py**
- **Propósito**: Define configuraciones globales del proyecto, como rutas para archivos temporales o parámetros del servidor.
- **Detalles técnicos**: 
  - Establece rutas como `TEMP_PDF_PATH` para guardar archivos subidos.
  - Puede incluir claves para integraciones externas o configuración específica para modelos de IA.

### **app/initialization.py**
- **Propósito**: Inicializa servicios y dependencias como el índice FAISS y los modelos de lenguaje.
- **Detalles técnicos**:
  - Carga los modelos de IA disponibles (`OllamaModel`, SmolLM, etc.).
  - Configura FAISS para manejar búsquedas eficientes en grandes volúmenes de datos.

### **app/main.py**
- **Propósito**: Punto de entrada principal para iniciar la API de FastAPI.
- **Detalles técnicos**:
  - Configura las rutas para subir PDFs (`/pdf`) y realizar consultas (`/query`).
  - Incluye metadatos como título, descripción y versión de la API.
  - Ejecuta los procesos necesarios al iniciar el servidor.

---

### **Rutas**

#### **app/routes/pdf.py**
- **Propósito**: Maneja la subida y procesamiento de archivos PDF.
- **Detalles técnicos**:
  - Acepta archivos PDF, los guarda temporalmente y los procesa con `pdf_service`.
  - Valida extensiones de archivo y maneja errores.
  - Endpoint: `/pdf/upload`.

#### **app/routes/query.py**
- **Propósito**: Permite a los usuarios realizar consultas utilizando los modelos de lenguaje y el índice RAG.
- **Detalles técnicos**:
  - Realiza búsquedas en FAISS para obtener fragmentos relevantes.
  - Genera respuestas utilizando modelos de lenguaje como `llama2` o `SmolLM`.
  - Endpoint: `/query`.

---

### **Servicios**

#### **app/services/pdf_service.py**
- **Propósito**: Procesa PDFs subidos, extrayendo texto y añadiéndolos al índice FAISS.
- **Detalles técnicos**:
  - Convierte PDFs a texto utilizando bibliotecas como `PyPDF2`.
  - Indexa los datos extraídos en FAISS para consultas posteriores.

#### **app/services/query_service.py**
- **Propósito**: Gestiona consultas al índice FAISS y modelos generativos.
- **Detalles técnicos**:
  - Busca fragmentos relevantes en FAISS utilizando las palabras clave de la consulta.
  - Genera respuestas con el modelo de lenguaje seleccionado.
  - Optimiza búsquedas y respuesta a preguntas para garantizar eficiencia.

---

### **Modelos**

#### **app/models/ollama_model.py**
- **Propósito**: Implementa una clase para interactuar con modelos de lenguaje alojados en Ollama.
- **Detalles técnicos**:
  - Permite ejecutar modelos como `SmolLM` y `llama3` desde Ollama.
  - Proporciona métodos para generar texto basado en prompts personalizados.

---

### **Utilidades**

#### **app/utils/translation.py**
- **Propósito**: Maneja traducciones entre idiomas para preguntas y respuestas.
- **Detalles técnicos**:
  - Utiliza APIs externas o modelos de traducción locales para soportar múltiples idiomas.

#### **app/utils/faiss_index.py**
- **Propósito**: Configura y gestiona el índice FAISS para búsqueda de fragmentos relevantes.
- **Detalles técnicos**:
  - Indexa texto extraído de PDFs para búsquedas rápidas.
  - Ofrece métodos para agregar, eliminar y buscar datos.

---

## Cómo Funciona

1. **Carga de datos (PDFs)**:
   - Los archivos subidos a `/pdf/upload` se procesan con `pdf_service.py`.
   - El texto extraído se indexa en FAISS, lo que permite búsquedas rápidas de texto relevante.

2. **Búsquedas en el índice**:
   - Cuando un usuario hace una consulta a `/query`, se busca en FAISS para encontrar fragmentos relevantes del texto previamente indexado.

3. **Generación de respuestas**:
   - Los fragmentos relevantes se pasan como contexto a un modelo de lenguaje (e.g., `SmolLM`, `llama2`).
   - El modelo genera una respuesta basada en el contexto y la pregunta del usuario.

4. **Optimización**:
   - FAISS acelera la búsqueda de texto relevante.
   - Modelos ligeros como `SmolLM` o configuraciones multihilo mejoran la velocidad de respuesta.

---

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

---

## Instalación

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/tu_usuario/tu_proyecto.git](https://github.com/CarlosSuarezCWH/InsightBot.git)
   cd InsightBot
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las rutas y claves necesarias en `config.py`.

---

## Uso

1. Inicia el servidor:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Sube un archivo PDF:
   - Endpoint: `POST /pdf/upload`
   - Ejemplo:
     ```bash
     curl -X POST -F "file=@documento.pdf" http://localhost:8000/pdf/upload
     ```

3. Realiza una consulta:
   - Endpoint: `POST /query/`
   - Ejemplo:
     ```bash
     curl -X POST "http://localhost:8000/query/?question=Tu+pregunta&model_name=llama2"
     ```

4. Explora la documentación interactiva:
   - Visita: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Contribución

1. Crea un fork del repositorio.
2. Haz tus cambios en una rama.
3. Envía un pull request.

---
