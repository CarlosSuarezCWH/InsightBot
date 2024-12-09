import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.initialization import pdf_service
from app.config import Config

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint para subir y procesar un archivo PDF.
    """
    print("[DEBUG] upload_pdf: Iniciando procesamiento del archivo.")

    try:
        # Verifica que el archivo sea un PDF
        print(f"[DEBUG] upload_pdf: Verificando si el archivo '{file.filename}' es un PDF.")
        if not file.filename.endswith(".pdf"):
            print("[ERROR] upload_pdf: El archivo no tiene extensión .pdf.")
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")
        
        # Guarda el archivo PDF temporalmente
        file_path = os.path.join(Config.TEMP_PDF_PATH, file.filename)
        print(f"[DEBUG] upload_pdf: Guardando archivo en la ruta temporal: {file_path}.")
        os.makedirs(Config.TEMP_PDF_PATH, exist_ok=True)  # Asegura que el directorio exista
        with open(file_path, "wb") as f:
            f.write(await file.read())
        print("[DEBUG] upload_pdf: Archivo guardado exitosamente.")
        
        # Procesa el archivo PDF
        print("[DEBUG] upload_pdf: Procesando el archivo PDF con pdf_service.process_pdf.")
        pdf_service.process_pdf(file_path)
        print("[DEBUG] upload_pdf: Archivo procesado y añadido al índice con éxito.")

        return {"message": "PDF procesado y añadido al índice con éxito"}
    
    except Exception as e:
        print(f"[ERROR] upload_pdf: Error al procesar el archivo PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo PDF: {str(e)}")
