FROM python:3.11-slim-bullseye

# Instala dependências do sistema para Kivy
RUN apt-get update && apt-get install -y \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libgl1-mesa-dev libgles2-mesa-dev libmtdev1 zlib1g-dev \
    libavformat-dev libavcodec-dev libswscale-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-libav \
    libgstreamer1.0-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /usr/src/marmos

# Copia o app e dependências
COPY ./app /usr/src/marmos/app
WORKDIR /usr/src/marmos/app

# Instala dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "main.py"]
