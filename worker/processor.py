import time
import boto3
from config import AWS_REGION, DYNAMODB_TABLE, SQS_QUEUE
from botocore.exceptions import ClientError

def esperar_fila(sqs, nome_fila):
    while True:
        try:
            print(f"🔍 Verificando existência da fila '{nome_fila}'...")
            url = sqs.get_queue_url(QueueName=nome_fila)['QueueUrl']
            print(f"✅ Fila '{nome_fila}' pronta: {url}")
            return url
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print("⏳ Fila ainda não disponível, aguardando...")
                time.sleep(2)
            else:
                raise

# Configuração boto3 
session = boto3.Session(
    aws_access_key_id="joao",
    aws_secret_access_key="joao",
    region_name=AWS_REGION
)

sqs = session.client("sqs", endpoint_url="http://localstack:4566")
dynamodb = session.resource("dynamodb", endpoint_url="http://localstack:4566")

queue_url = esperar_fila(sqs, SQS_QUEUE)

def processar_usuarios():
    print("Iniciando processamento de pedidos...")
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        messages = response.get("Messages", [])
        for msg in messages:
            user_id = msg["Body"]
            tabela = dynamodb.Table(DYNAMODB_TABLE)
            usuario = tabela.get_item(Key={"id": user_id}).get("Item")

            if not usuario:
                print(f"Usuario {user_id} não encontrado.")
                continue

            # Remover da fila
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )

            print(f"Usuario {user_id} processado.")
        time.sleep(60)

if __name__ == "__main__":
    processar_usuarios()
