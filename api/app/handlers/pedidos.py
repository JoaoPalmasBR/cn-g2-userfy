import uuid
from app.utils.aws import dynamodb, sqs, s3
from app import config
from app.schemas import PedidoInput
from fastapi import HTTPException

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
        
        # Log de sucesso (opcional)
        with open("teste.txt", "a") as f:
            f.write(f"Pedido criado com ID: ")
        # Supondo que você tenha um cliente S3 chamado s3 no app.utils.aws
        print("antes s3")
        s3.upload_file(
            Filename="teste.txt",
            Bucket=config.S3_BUCKET,
            Key="logs/{}.txt".format(pedido_id)
        )
        print("depois s3")
        return {"id": pedido_id, "status": "recebido"}

    except Exception as e:
        print(f"Erro ao criar pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar pedido.")
