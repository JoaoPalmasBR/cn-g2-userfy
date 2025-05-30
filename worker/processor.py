import time
import boto3
from reportlab.pdfgen import canvas
from config import AWS_REGION, DYNAMODB_TABLE, SQS_QUEUE, S3_BUCKET



# Configuração boto3
session = boto3.Session(
    aws_access_key_id="joao",
    aws_secret_access_key="joao",
    region_name=AWS_REGION
)

sqs = session.client("sqs", endpoint_url="http://localstack:4566")
dynamodb = session.resource("dynamodb", endpoint_url="http://localstack:4566")
s3 = session.client("s3", endpoint_url="http://localstack:4566")

queue_url = f"http://localstack:4566/000000000000/{SQS_QUEUE}"

def gerar_pdf(pedido):
    file_path = f"/tmp/{pedido['id']}.pdf"
    c = canvas.Canvas(file_path)
    c.drawString(100, 750, f"Pedido: {pedido['id']}")
    c.drawString(100, 730, f"Cliente: {pedido['cliente']}")
    c.drawString(100, 710, f"Mesa: {pedido['mesa']}")
    c.drawString(100, 690, f"Itens: {', '.join(pedido['itens'])}")
    c.save()
    return file_path

def processar_pedidos():
    print("Iniciando processamento de pedidos...")
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        messages = response.get("Messages", [])
        for msg in messages:
            pedido_id = msg["Body"]
            tabela = dynamodb.Table(DYNAMODB_TABLE)
            pedido = tabela.get_item(Key={"id": pedido_id}).get("Item")

            if not pedido:
                print(f"Pedido {pedido_id} não encontrado.")
                continue

            print("antes do pdf")
            # Gerar e salvar PDF no S3
            pdf_path = gerar_pdf(pedido)
            with open(pdf_path, "rb") as f:
                s3.upload_fileobj(f, S3_BUCKET, f"{pedido_id}.pdf")
            print("depois do pdf")
            
            # Atualizar status no DynamoDB
            tabela.update_item(
                Key={"id": pedido_id},
                UpdateExpression="SET #s = :s",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":s": "concluído"}
            )

            # Remover da fila
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg["ReceiptHandle"]
            )

            print(f"Pedido {pedido_id} processado.")
        time.sleep(2)

if __name__ == "__main__":
    processar_pedidos()
