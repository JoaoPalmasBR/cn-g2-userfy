from fastapi import FastAPI
from app.handlers.pedidos import criar_pedido
from app.schemas import PedidoInput
from app.routes.comprovantes import router as comprovantes_router
import boto3
from app.utils.aws import dynamodb, sns
from app import config
import json

app = FastAPI()
app.include_router(comprovantes_router)

sns_client = boto3.client('sns', endpoint_url='http://localstack:4566', region_name='us-east-1')

@app.post("/pedidos")
async def post_pedido(pedido: PedidoInput):
    return criar_pedido(pedido)

@app.put("/pedidos/{pedido_id}/concluir", tags=["Pedidos"])
def concluir_pedido(pedido_id: str):
    try:
        tabela = dynamodb.Table(config.DYNAMODB_TABLE)

        # Atualiza o status para "concluído"
        tabela.update_item(
            Key={"id": pedido_id},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": "concluído"}
        )

        # Publica no SNS
        topicarn = 'arn:aws:sns:us-east-1:000000000000:PedidosConcluidos'
        message1 = f'Novo pedido concluído: {pedido_id}'
        subject1 = 'Pedido Pronto!'

        response = sns_client.publish(
            TopicArn = topicarn,
            Message = message1,
            Subject=subject1
        )
        
        print(f"Notificação SNS enviada para pedido {pedido_id}, response={response}")
        print("do formato que o deliberado quer")
        print({
    "TopicArn": topicarn,
    "Message": message1,
    "Subject": subject1
})
        

        return {"id": pedido_id, "status": "concluído", "sns_message_id": response.get("MessageId")}

    except Exception as e:
        print(f"Erro ao concluir pedido: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao concluir pedido.")