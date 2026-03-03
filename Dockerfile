# 1. Usamos a imagem base do Python 3.10
FROM python:3.10-slim

# 2. Definimos a pasta de trabalho
WORKDIR /app

# 3. [ATUALIZADO] Instalação das bibliotecas gráficas do Linux
# Adicionamos o libosmesa6 e libegl1 para renderização 3D sem monitor!
RUN apt-get update && apt-get install -y \
    libx11-6 \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    libxext6 \
    libsm6 \
    libice6 \
    libxt6 \
    libosmesa6 \
    libegl1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamos todos os arquivos do projeto para o Docker
COPY . .

# 5. Instalamos o Slicer (O arquivo Linux)
RUN pip install vtk_mrml-9.4.0-cp310-cp310-manylinux_2_35_x86_64.whl

# 6. Instalamos o restante das bibliotecas do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 7. Configuramos o caminho do Python
ENV PYTHONPATH="."

# 8. Expomos a porta da aplicação
EXPOSE 8080

# 9. Comando para iniciar o programa
CMD ["python", "examples/medical_viewer_app.py", "--host", "0.0.0.0", "--port", "8080"]