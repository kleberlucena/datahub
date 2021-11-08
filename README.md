# Template de sistemas internos à COINT

**Template voltado para projetos internos, integrados ao Ambiente de Aplicativos da PMPB.**


## Projeto

### Guia de instalação do projeto

Este projeto foi reproduzido em ambiente Ubuntu 20.04.

## Instalando o projeto utilizando Docker

**Pré-requisitos:**

- Docker
- docker-compose

Para iniciar a aplicação, apenas execute o comando:

```shell
docker-compose up
```

Com os containers rodando, execute o seguinte comando de criação de um usuário admin do django.
O comando a seguir precisa ser executado dentro do mesmo diretório do projeto onde o arquivo `docker-compose.yml` está localizado:

```shell
docker-compose run web python manage.py createsuperuser
```

Caso você deseje executar o comando acima no servidor de stage ou production, você precisa exportar as variáveis de ambiente
exigidas pelo arquivo `docker-compose.yml`. Verifique as variáveis do arquivo e execute o comando assim:

```shell
DB_PASSWORD=SENHA_DO_BANCO \
IMAGE_TAG=TAG_DA_IMAGEM_DOCKER_AQUI \
docker-compose run web python manage.py createsuperuser
```

Agora abra seu navegador e acesse **http://localhost:8000**


### Diretamente na sua máquina

**Necessário o Python na máquina, no Ubuntu já vem por padrão**

Caso não tenha no sistema operacional consulte:

https://www.python.org/downloads/

A versão do python utilizada para o projeto: **3.8.2 64-bits para Linux**

Opcional, mas utilizado: [pyenv](https://github.com/pyenv/pyenv), gerenciador de versões para o python

[Instalador automático do pyenv](https://github.com/pyenv/pyenv-installer)

[Pré-requisitos para o pyenv](https://github.com/pyenv/pyenv/wiki/Common-build-problems)

**Pré-requisitos**:

- Git
- Postgres 10
- Python 3.8

Opcional, mas utilizado: **ambiente virtualizado em python**

para criar um ambiente virtualizado do python na pasta do projeto:

```shell
python -m venv venv
```

Onde logo em seguida ativamos usando:

```shell
source venv/bin/activate
```


#### Instalando as dependências do projeto


Na pasta da raiz do projeto, instale as dependencias:

```shell
pip install -r requirements.txt
```

#### Configurando variáveis de ambiente

Copie o arquivo `.env.example`, cole na pasta project e renomei para `.env` e configure as variáveis de embiente presentes nele:

```shell
DEBUG=on
SECRET_KEY=sua_chave_secreta_aqui
# Configurações do banco
DB_NAME=django
DB_USER=django
DB_PASSWORD=django
DB_HOST=db
DB_PORT=5432
```

No caso da chave secreta, insira caracteres aleatórios, não podendo conter espaços **(Crie uma chave forte)**.

#### Migrando as tabelas

Na pasta raiz do projeto:

```
python manage.py migrate
```

#### Criando o superusário

Para acessar o sistema, deve-se primeiramente criar um superusuário:
```
python manage.py createsuperuser
```

#### Para rodar a aplicação

```
python manage.py runserver"
```

#### Para rodar a aplicação e ela ser acessível na rede local

```
python manage.py runserver 0.0.0.0:8000"
```

Agora acesse: http://localhost:8000


#### Para coletar os staticos da aplicação e enviar para o minio 

```
python manage.py collectstatic
```

## Autores

- **Diogenes Sousa** - *Desenvolvedor* e *Gerente de Projetos*
- **Jovennan Ramalho** - *Desenvolvedor* e *Analista de Sistemas*


## Licença

Todos os direitos reservados a PMPB.
