FROM python:3.8-slim
# Configurando PYTHONUNBUFFERED com qualquer valor diferente de vazio
# faz com que o Python lance todos os seus logs direto para terminal
# evitando o buffer. Isso nos ajuda a ver os logs direto no container imediatamente.
# ou seja, os logs da nossa aplicação Django podem ser vistos em tempo real sem delay.
ENV PYTHONUNBUFFERED=1
RUN apt update -y \
  && apt install binutils \
  && apt install -y \
  libproj-dev \
  gdal-bin \
  geos-3.8.0 \
  proj6 \
  build-essential
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
