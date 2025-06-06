import uuid
from app.utils.aws import dynamodb, sqs, s3
from app import config
from app.schemas import PedidoInput
from fastapi import HTTPException
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# def criar_pedido(pedido: PedidoInput):
#     pedido_id = str(uuid.uuid4())
    
#     # Grava no DynamoDB
#     tabela = dynamodb.Table(config.DYNAMODB_TABLE)
#     tabela.put_item(Item={
#         "id": pedido_id,
#         "cliente": pedido.cliente,
#         "itens": pedido.itens,
#         "mesa": pedido.mesa,
#         "status": "pendente"
#     })

#     # Envia para SQS
#     sqs.send_message(
#         QueueUrl=f"http://localstack:4566/000000000000/{config.SQS_QUEUE}",
#         MessageBody=pedido_id,
#         MessageGroupId="pedidos"  # Necessário para filas FIFO
#     )

#     return {"id": pedido_id, "status": "recebido"}

def criar_pedido(pedido: PedidoInput):
    try:
        pedido_id = str(uuid.uuid4())

        # Grava no DynamoDB
        tabela = dynamodb.Table(config.DYNAMODB_TABLE)
        tabela.put_item(Item={
            "id": pedido_id,
            "cliente": pedido.cliente,
            "itens": pedido.itens,
            "mesa": pedido.mesa,
            "status": "pendente"
        })

        # Envia para SQS
        sqs.send_message(
            QueueUrl=f"http://localstack:4566/000000000000/{config.SQS_QUEUE}",
            MessageBody=pedido_id,
            MessageGroupId="pedidos"
        )
        
        pdf_filename = pedido_id+".pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, f"Pedido: {pedido_id} \n")
        c.drawString(100, 730, f"Cliente: {pedido.cliente} \n")
        c.drawString(100, 710, f"Status: pendente\n")
        c.drawString(100, 690, f"Mesa: {pedido.mesa}\n")
        c.drawString(100, 670, f"Itens: {', '.join(pedido.itens)}\n")
        c.save()
        # Log de sucesso (opcional)
        # with open("teste.txt", "a") as f:
            # f.write(f"Pedido criado com ID: ")
        # Supondo que você tenha um cliente S3 chamado s3 no app.utils.aws
        print("antes s3")
        s3.upload_file(
            Filename=pdf_filename,
            Bucket=config.S3_BUCKET,
            Key="logs/{}".format(pdf_filename)
        )
        print("depois s3")
        return {"id": pedido_id, "status": "recebido"}

    except Exception as e:
        print(f"Erro ao criar pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar pedido.")
