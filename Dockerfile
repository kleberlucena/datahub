FROM python:3.8-slim-bullseye
# Configurando PYTHONUNBUFFERED com qualquer valor diferente de vazio
# faz com que o Python lance todos os seus logs direto para terminal
# evitando o buffer. Isso nos ajuda a ver os logs direto no container imediatamente.
# ou seja, os logs da nossa aplicação Django podem ser vistos em tempo real sem delay.
ENV PYTHONUNBUFFERED=1

# Instalação de bibliotecas necessárias para funcionamento do Postgis
RUN apt-get update \
  && apt-get install -y binutils \
  && apt-get install -y gdal-bin \
  && apt-get install -y libproj-dev \
  && apt-get install -y postgis \
  && apt-get install -y postgresql-13-postgis-3 \
  && apt-get install -y postgresql-13-postgis-3-scripts \
  && apt-get install -y build-essential

RUN mkdir /code
WORKDIR /code
COPY requirements_prod.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements_prod.txt
COPY . /code/

