# Documentação do bacinf

## Sumário

1. [Módulo de Entidades](./entity.md)

## Recomendações Gerais


1- Após levantar o serviço com o comando "python manage.py runserver", se faz necessário executar o comando:
* celery -A project worker -l info
Esse comando levant ao serviço celery e deixa disponível as execuções de tarefas em paralelo.

Continua...

