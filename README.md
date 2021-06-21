# Arquitetura em microserviços

Projeto para finalidade de testes que consiste em 2 microserviços que possibilitam realizar uma consulta entre um médico e um paciente e gerar uma entrada financeira de cobrança da consulta.

Quando uma consulta é finalizada, é realizada uma notificação para a criação de uma cobrança no serviço financeiro.

## Tecnologias utilizadas

Para o desenvolvimento do projeto foi utilizado Python 3.8.6, e as seguintes dependências:

- Desenvolvimento e servidor das aplicações de api:
    - FastAPI
    - Uvicorn
- Base de dados e suas migrações:
    - PostgreSQL 13.0
    - asyncpg
    - yoyo-migrations
    - psycopg2
- Mensageria entre as aplicações:
    - RabbitMQ 3.8
    - aio-pika
- Configuração de ambientes virtuais e variáveis:
    - dynaconf
    - pipenv
- Testes
    - pytest
    - pytest-asyncio
    - httpx

## Setup das aplicações

### Utilizando docker-compose
Para realizar o setup utilizando docker, basta apenas renomear o arquivo `.env.example`, da pasta raíz, para `.env` e configurar as variáveis de ambiente de acordo. Após isso levantar os containers:

```console
user@domain:~$ docker-compose up --build -d
```

### Localmente
Para levantar as aplicações localmente, é necessário realizar a instalação do [pipenv](https://pipenv.pypa.io/en/latest/basics/), e instalar os pacotes em cada aplicação a partir dele:

```console
user@domain:~/appointment-api/appointment$ pipenv install
user@domain:~/appointment-api/billing$ pipenv install
```

A partir disso, alterar os arquivos `.env.example` de cada aplicação para `.env` e configurar as váriaveis de ambiente de acordo. E enfim subir as devidas aplicações via pipenv:

```console
user@domain:~/appointment-api/appointment$ pipenv run python server.py
user@domain:~/appointment-api/billing$ pipenv run python server.py
```

### Migrações da base de dados

Para realizar as migrações da base de dados, é necessário rodar individualmente para cada projeto.
Pelo docker, basta apenas rodar as imagens `appointment-migrations` e `billing-migrations`.

Localmente, utilizamos os scripts de migrations via pipenv:

```console
user@domain:~/appointment-api/appointment$ pipenv run python migrations/db_upgrade.py
user@domain:~/appointment-api/billing$ pipenv run python migrations/db_upgrade.py
``` 

## Testes

Para realizar os testes das aplicações, utilizamos o pytest dentro pipenv para cada aplicação:

```console
user@domain:~/appointment-api/appointment$ pipenv run pytest
user@domain:~/appointment-api/billing$ pipenv run pytest
``` 

### Documentação

As documentações das rotas das apis estarão disponíveis via Swagger em `/docs`, assim como via Redoc em `/redoc`.
