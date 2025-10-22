import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import argparse

# --- CONFIGURACIÓN DE TESSERACT ---
# Asegúrate de que Tesseract esté instalado y accesible.
# En Windows, podrías necesitar descomentar y ajustar la siguiente línea:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# En Linux/macOS, generalmente se encuentra en el PATH si se instala con un gestor de paquetes.
try:
    # Intenta obtener la versión para verificar que tesseract es accesible
    pytesseract.get_tesseract_version()
except pytesseract.TesseractNotFoundError:
    print(
        " Error: Tesseract no está instalado o no se encuentra en el PATH del sistema."
    )
    print(
        "Por favor, instala Tesseract OCR y asegúrate de que su ejecutable esté en el PATH."
    )
    exit(1)


def extraer_texto_pdf_con_ocr(ruta_pdf: str) -> str:
    """
    Extrae texto de un PDF, incluyendo el texto dentro de las imágenes usando OCR.

    Args:
        ruta_pdf: La ruta al archivo PDF.

    Returns:
        Una cadena de texto con todo el contenido extraído del PDF.
    """
    texto_completo = ""
    try:
        documento = fitz.open(ruta_pdf)
        print(
            f" Procesando archivo: '{os.path.basename(ruta_pdf)}' ({len(documento)} páginas)..."
        )

        for num_pagina, pagina in enumerate(documento): # pyright: ignore[reportArgumentType]
            texto_completo += f"--- Página {num_pagina + 1} ---\n\n"

            # 1. Extraer texto digital
            texto_completo += pagina.get_text() + "\n"

            # 2. Extraer texto de imágenes con OCR
            imagenes = pagina.get_images(full=True)
            if not imagenes:
                continue

            print(
                f"  -> Página {num_pagina + 1}: {len(imagenes)} imágenes encontradas para OCR."
            )
            for i, img_info in enumerate(imagenes):
                xref = img_info[0]
                base_imagen = documento.extract_image(xref)
                bytes_imagen = base_imagen["image"]

                try:
                    imagen_obj = Image.open(io.BytesIO(bytes_imagen))
                    # 'spa' para español. Cambia a 'eng' para inglés si es necesario.
                    texto_imagen = pytesseract.image_to_string(
                        imagen_obj, lang="spa"
                    )
                    if texto_imagen.strip():
                        texto_completo += f"\n--- Texto de Imagen {i+1} (OCR) ---\n"
                        texto_completo += texto_imagen + "\n"
                except Exception as img_e:
                    print(f"    - No se pudo procesar la imagen {i+1} en la página {num_pagina + 1}: {img_e}")


        return texto_completo

    except Exception as e:
        print(f"Error inesperado al procesar el PDF '{ruta_pdf}': {e}")
        return ""


def guardar_texto(contenido: str, ruta_salida: str):
    """Guarda el contenido de texto en un archivo."""
    try:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f" Contenido guardado en: '{ruta_salida}'")
    except Exception as e:
        print(f"No se pudo guardar el archivo en '{ruta_salida}': {e}")


def main(input_path: str):
    """
    Función principal que procesa un archivo PDF o una carpeta de archivos PDF.
    """
    if not os.path.exists(input_path):
        print(f"Error: La ruta especificada no existe: '{input_path}'")
        return

    # --- Lógica para procesar una CARPETA ---
    if os.path.isdir(input_path):
        print(f"Procesando carpeta: '{input_path}'")
        
        # Crear la carpeta de salida
        folder_name = os.path.basename(os.path.normpath(input_path))
        output_dir = input_path #f"{folder_name}"
        os.makedirs(output_dir, exist_ok=True)
        print(f"Los resultados se guardarán en: '{output_dir}'")

        # Iterar sobre los archivos de la carpeta
        pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith(".pdf")]
        if not pdf_files:
            print("No se encontraron archivos PDF en la carpeta.")
            return
            
        for filename in pdf_files:
            pdf_path = os.path.join(input_path, filename)
            
            # Extraer contenido
            contenido_extraido = extraer_texto_pdf_con_ocr(pdf_path)

            if contenido_extraido:
                # Definir ruta de salida
                base_name, _ = os.path.splitext(filename)
                output_txt_path = os.path.join(output_dir, f"{base_name}.txt")
                # Guardar el resultado
                guardar_texto(contenido_extraido, output_txt_path)

    # --- Lógica para procesar un ARCHIVO ---
    elif os.path.isfile(input_path):
        if not input_path.lower().endswith(".pdf"):
            print(f"Error: El archivo proporcionado no es un PDF: '{input_path}'")
            return
            
        # Extraer contenido
        contenido_extraido = extraer_texto_pdf_con_ocr(input_path)

        if contenido_extraido:
            # Definir ruta de salida
            base_name, _ = os.path.splitext(input_path)
            output_txt_path = f"{base_name}.txt"
            # Guardar el resultado
            guardar_texto(contenido_extraido, output_txt_path)
    
    else:
        print(f"Error: La ruta no es un archivo ni una carpeta válida: '{input_path}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extrae texto de archivos PDF usando OCR. "
        "Acepta un archivo PDF o una carpeta que contenga archivos PDF."
    )
    parser.add_argument(
        "ruta_entrada",
        type=str,
        help="La ruta al archivo PDF o a la carpeta que se va a procesar.",
    )

    args = parser.parse_args()
    main(args.ruta_entrada)