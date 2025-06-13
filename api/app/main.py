from fastapi import FastAPI, HTTPException
from app.schemas import UserInput
import boto3
from app.utils.aws import dynamodb, sqs
from app import config
import uuid
from botocore.exceptions import ClientError


app = FastAPI()

sns_client = boto3.client('sns', endpoint_url='http://localstack:4566', region_name='us-east-1')

@app.post("/users")
async def post_user(user: UserInput):
    try:
        user_id = str(uuid.uuid4())
        # Grava no DynamoDB
        tabela = dynamodb.Table(config.DYNAMODB_TABLE)
        tabela.put_item(Item={
            "id": user_id,
            "nome": user.nome,
            "email": user.email
        })
        # Log de sucesso (opcional)
        print(f"Usuario criado com ID: {user_id}")
        # Envia para SQS
        sqs.send_message(
            QueueUrl=f"http://localstack:4566/000000000000/{config.SQS_QUEUE}",
            MessageBody=user_id,
            MessageGroupId="Users"
        )
        return {"id": user_id, "status": "recebido"}

    except Exception as e:
        print(f"Erro ao criar usuario: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar usuario.")
@app.get("/users")
def listar_users():
    try:
        # listar usuarios no DynamoDB
        dynamodb = boto3.resource(
            'dynamodb',
            region_name="us-east-1",
            endpoint_url="http://localstack:4566"
        )
        DYNAMODB_TABLE = dynamodb.Table("Users")

        response = DYNAMODB_TABLE.scan()
        # print(response)
        usuarios = response.get("Items", [])
        return [
            {
                "id": user["id"],
                "nome": user["nome"],
                "email": user["email"]
            }
            for user in usuarios
        ]
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return []
        raise