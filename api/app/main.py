from fastapi import FastAPI
from app.handlers.pedidos import criar_pedido
from app.schemas import PedidoInput
from app.routes.comprovantes import router as comprovantes_router

app = FastAPI()
app.include_router(comprovantes_router)

@app.post("/pedidos")
async def post_pedido(pedido: PedidoInput):
    return criar_pedido(pedido)
