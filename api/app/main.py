from fastapi import FastAPI
from app.handlers.pedidos import criar_pedido
from app.schemas import PedidoInput
from app.routes.comprovantes import router as comprovantes_router

app = FastAPI()
app.include_router(comprovantes_router)

@app.post("/pedidos")
async def post_pedido(pedido: PedidoInput):
    return criar_pedido(pedido)

@app.put("/pedidos/{pedido_id}")
async def put_pedido(pedido_id: int, pedido: PedidoInput):
    # Aqui voce pode implementar atualização do status do pedido para "concluido"
    return concluir_pedido(pedido_id, pedido)