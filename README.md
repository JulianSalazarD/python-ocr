# Extractor de Texto PDF con OCR

Este proyecto es un script de Python que extrae texto de archivos PDF. Su principal característica es que no solo extrae el texto digital (texto seleccionable), sino que también utiliza Tesseract OCR para extraer texto de las imágenes incrustadas dentro del PDF.

El script puede procesar un único archivo PDF o una carpeta completa de archivos PDF, generando un archivo .txt por cada documento procesado.

---

## Características

- **Extracción Híbrida:** Combina la extracción de texto digital (usando PyMuPDF) con el Reconocimiento Óptico de Caracteres (usando Tesseract) para una cobertura completa.

- **Procesamiento por Lotes:** Capaz de procesar una carpeta entera de archivos PDF de una sola vez.

- **Procesamiento de Archivo Único:** Puede apuntar a un solo archivo PDF.

- **Contenerizado:** Incluye un Dockerfile para construir y ejecutar la aplicación en un entorno aislado sin necesidad de instalar dependencias localmente.

---

## Archivos del Proyecto

- `main.py`: El script principal de Python que contiene toda la lógica de extracción.

- `requirements.txt`: La lista de dependencias de Python.

- `Dockerfile`: El archivo de configuración para construir la imagen de Docker.

---

## Requisitos y Configuración

Tienes dos formas de ejecutar este proyecto: Localmente o usando Docker.

### 1. Ejecución Local

**Dependencias del Sistema**

Primero, debes instalar Tesseract OCR en tu sistema.

- **Windows**: Descarga el instalador desde UB-Mannheim-Tesseract. Asegúrate de que tesseract.exe esté en el PATH del sistema o ajusta la ruta en el script main.py.

- **Linux (Debian/Ubuntu)**:

```Bash

sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-spa
```

- **macOS (usando Homebrew)**:

```Bash
brew install tesseract
brew install tesseract-lang # (O instala directamente tesseract-spa)
```
- **Dependencias de Python**

Se recomienda usar un entorno virtual.

```Bash
# 1. Crea un entorno virtual
python -m venv venv
# 2. Actívalo
# En Windows (CMD):
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# 3. Instala las librerías de Python
pip install -r requirements.txt
```
Asegúrate de que tu archivo requirements.txt contenga lo siguiente:

```
Plaintext
PyMuPDF
pytesseract
Pillow
```

### 2. Ejecución con Docker

Esta es la forma más fácil, ya que todas las dependencias (Python y Tesseract) se instalan dentro del contenedor.

---

## Uso

### Uso Local

El script se ejecuta desde la línea de comandos y acepta una ruta (a un archivo o a una carpeta) como argumento.

```Bash

# Para procesar un solo archivo PDF
python main.py ruta/a/mi/documento.pdf

# Para procesar todos los PDFs en una carpeta
python main.py ruta/a/la/carpeta/
```

Los resultados se guardarán como archivos .txt en la misma ubicación que los archivos PDF originales.

### Uso con Docker

- Construye la imagen de Docker: Desde la carpeta raíz de tu proyecto (donde está el Dockerfile), ejecuta:

```Bash

docker build -t ocr-extractor .
```

- **Prepara tus archivos**: Crea una carpeta (ej. mis_pdfs) y coloca allí todos los PDF que quieras procesar.

```Bash
# --- Para Linux/macOS ---
# $(pwd) usa tu directorio de trabajo actual
docker run --rm -v "$./mis_pdfs":/mis_pdfs ocr-extractor /mis_pdfs

# --- Para Windows (CMD) ---
# %cd% usa tu directorio de trabajo actual
docker run --rm -v ".\mis_pdfs":/mis_pdfs ocr-extractor /mis_pdfs
```

Si solo quieres procesar un archivo específico dentro de esa carpeta:

```Bash

# (Ejemplo en Linux/macOS)
docker run --rm -v "./mis_pdfs":/mis_pdfs ocr-extractor /mis_psfs/mi_archivo_especifico.pdf
```
Al terminar, los archivos .txt con el texto extraído aparecerán en tu carpeta local mis_pdfs.

---

## Configuración del Idioma

Por defecto, el script está configurado para usar el idioma español (lang="spa") para el OCR.

Si necesitas procesar PDFs en otro idioma (ej. inglés):

- En `main.py`: Cambia la línea `texto_imagen = pytesseract.image_to_string(...)` para que use `lang="eng"`.

- En `dockerfile`: Añade el paquete de idioma correspondiente, por ejemplo `tesseract-ocr-eng`, a la lista `apt-get install`.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.