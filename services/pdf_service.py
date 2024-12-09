import os
import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer

class PDFService:
    def __init__(self, temp_pdf_path, faiss_index_path, query_service):
        """
        Inicializa el servicio de procesamiento de PDFs.

        :param temp_pdf_path: Ruta temporal para almacenar los PDFs.
        :param faiss_index_path: Ruta al índice FAISS.
        :param query_service: Instancia del servicio de consultas.
        """
        self.temp_pdf_path = temp_pdf_path
        self.faiss_index_path = faiss_index_path
        self.query_service = query_service
        print("[DEBUG] PDFService: Cargando el modelo de embeddings 'all-MiniLM-L6-v2'.")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo para embeddings
        print("[DEBUG] PDFService: Modelo de embeddings cargado exitosamente.")

    def process_pdf(self, file_path):
        try:
            print(f"[DEBUG] process_pdf: Iniciando procesamiento del archivo PDF: {file_path}")

            # Verificar si el archivo existe
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"[ERROR] process_pdf: El archivo no existe: {file_path}")

            # Extraer texto
            print("[DEBUG] process_pdf: Abriendo el archivo PDF para extraer texto.")
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
                    print(f"[DEBUG] process_pdf: Texto extraído de la página {i + 1}.")
            
            if not text.strip():
                raise ValueError("[ERROR] process_pdf: El texto extraído del PDF está vacío.")
            
            # Dividir en fragmentos
            print("[DEBUG] process_pdf: Dividiendo el texto en fragmentos.")
            fragments = [text[i:i + 500] for i in range(0, len(text), 500)]
            if not fragments:
                raise ValueError("[ERROR] process_pdf: No se generaron fragmentos del PDF. Verifique el contenido del archivo.")
            
            print(f"[DEBUG] process_pdf: Fragmentos generados: {len(fragments)}")
            for idx, fragment in enumerate(fragments[:5]):
                print(f"[DEBUG] Fragmento {idx + 1}:\n{fragment[:200]}...\n")

            # Limpiar índice FAISS y sincronizar fragmentos
            print("[DEBUG] process_pdf: Limpiando índice FAISS existente.")
            self.query_service.fragments.clear()
            self.query_service.index.reset()

            # Generar embeddings para los fragmentos
            print("[DEBUG] process_pdf: Generando embeddings para los fragmentos.")
            embeddings = self.embedding_model.encode(fragments, convert_to_tensor=False)
            embeddings = np.array(embeddings)
            print(f"[DEBUG] process_pdf: Embeddings generados: {embeddings.shape}")

            if embeddings.size == 0:
                raise ValueError("[ERROR] process_pdf: Los embeddings no se generaron correctamente.")
            
            # Añadir embeddings y fragmentos al índice
            print("[DEBUG] process_pdf: Añadiendo embeddings y fragmentos al índice FAISS.")
            self.query_service.add_to_index(embeddings, fragments)
            print("[INFO] process_pdf: Fragmentos añadidos al índice FAISS con éxito.")

            # Verificar sincronización
            print("[DEBUG] process_pdf: Verificando estado del índice y fragmentos después de sincronización.")
            print(f"[DEBUG] Vectores en índice FAISS: {self.query_service.index.ntotal}")
            print(f"[DEBUG] Fragmentos en QueryService: {len(self.query_service.fragments)}")

        except FileNotFoundError as fnf_error:
            print(f"[ERROR] process_pdf: Archivo no encontrado: {fnf_error}")
            raise fnf_error
        
        except ValueError as val_error:
            print(f"[ERROR] process_pdf: Error en el contenido o procesamiento del PDF: {val_error}")
            raise val_error

        except Exception as e:
            print(f"[ERROR] process_pdf: Error inesperado procesando el PDF: {e}")
            raise e
