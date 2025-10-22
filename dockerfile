# -- Etapa 1: Imagen Base --
# Usamos una imagen oficial de Python 3.14 sobre Debian.
# La versión "slim" es más ligera que la completa.
FROM python:3.14-slim-trixie

# -- Etapa 2: Instalar Dependencias del Sistema --
# Actualiza los paquetes del sistema para corregir vulnerabilidades.
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-spa \
    # Limpiamos la caché de apt para mantener la imagen pequeña.
    && rm -rf /var/lib/apt/lists/*

# -- Etapa 3: Configurar el Entorno de la Aplicación --
# Establecemos el directorio de trabajo dentro del contenedor.
WORKDIR /app

# -- Etapa 4: Instalar Dependencias de Python --
# Copiamos solo el archivo de requerimientos primero.
# Docker guardará esta capa en caché si el archivo no cambia, acelerando futuras compilaciones.
COPY requirements.txt .

# Instalamos las librerías de Python.
# --no-cache-dir reduce el tamaño de la imagen final.
RUN pip install --no-cache-dir -r requirements.txt

# -- Etapa 5: Copiar el Código de la Aplicación --
# Copiamos el resto de los archivos del proyecto (nuestro script .py) al contenedor.
COPY . .

# -- Etapa 6: Definir el Punto de Entrada --
# Esto configura el contenedor para que se comporte como un ejecutable.
# Al ejecutar el contenedor, se llamará a "python ocr_extractor.py".
# Los argumentos que pases al comando 'docker run' se añadirán al final.
ENTRYPOINT ["python", "main.py"]