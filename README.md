# UserFy

 Um projeto  aplicação simples de coleta
e persistência de dados em ambiente simulado de nuvem usando LocalStack, onde pedidos são processados por meio de serviços como SQS, DynamoDB, juntamente com uma API FastAPI em Python

URL de execução dos comandos POST e GET: http://localhost:8000/users

URL visão DOCS: http://localhost:8000/docks

## Passos para subir o ambiente

"Em um cenario que voce ja instalou o aws-cli, wsl, docker, pyhton (coisas que tive que fazer nesse computador antes de comecar kkkk)"


### Configurar o AWS CLI:
```bash
  aws configure
```
Vai pedir um nome, senha, regiao e formato de retorno:

```bash
  AWS Access Key ID: joao
  AWS Secret Access Key: joao
  Default region name: us-east-1
  Default output format: json
```

Rodar o docker compose:
```bash
  docker compose up --build
```

Isso vai subir:
- LocalStack
- FastAPI (User API)
- Worker (Processor)
- Init script para criar filas, tabelas e buckets

## Estrutura 

/userfy_api: API FastAPI com endpoints para cadastro e listagem de usuários.

/userfy_init: Cria recursos na inicialização (DynamoDB, SQS). "em tese"

/userfy_worker: Função Lambda que processa mensagens da fila.

### Requisiçoes
Aquele mesmo lembrete - quando criar o primeiro usuario da historia, ele da aquele erro de nao foi possivel criar, 2 segundos depois pode reexecutar o comando que funcionará normalmente
erro que aparece: "detail": "Erro interno ao processar usuario."

Criar um usuario:
```bash
  curl -X POST http://localhost:8000/users \
    -H "Content-Type: application/json" \
    -d '{"nome": "João", "email": "joao@foodz.com"}'
```
Resposta:
Codigo: 200

```json
  {
    "id": "e10c6b0f-4916-4bbe-8257-ab63d0dd2bd6",
    "status": "recebido"
  }
```

Listar usuarios criados
```bash
  curl -X 'GET' \
    'http://localhost:8000/users' \
    -H 'accept: application/json'
```
ou 
```bash
  curl http://localhost:8000/users

```
Resposta com um usuario:
```json
[
  {
    "id": "e10c6b0f-4916-4bbe-8257-ab63d0dd2bd6",
    "nome": "string",
    "email": "string"
  }
]
```
Resposta com multiplos usuarios:
```json
[
  {
    "id": "12ba6166-7670-4077-b430-db6b4888bc31",
    "nome": "string",
    "email": "string"
  },
  {
    "id": "a3e7a747-cb69-4098-9c8d-8448ecd508b9",
    "nome": "string",
    "email": "string"
  },
  {
    "id": "47b0b3e6-0912-4981-aa22-e9bee0bc0107",
    "nome": "string",
    "email": "string"
  }
]
```

```bash
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name Users
```

## Conceitos

- Serverless (funcao observadora Lambda)
- Fila de Mensagens	(comunicação assíncrona)
- Banco de Dados NoSQL (persistência de usuários)
- Lambda (processa mensagens)