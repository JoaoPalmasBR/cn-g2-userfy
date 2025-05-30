```bash
    curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "João",
    "itens": ["Pizza", "Refri"],
    "mesa": 5
  }'
```
```json
{
  "id": "c3aef3b4-xxxx-xxxx-xxxx-b45e8e3bdf04",
  "status": "recebido"
}
```

```bash
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name Pedidos
```

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://foodz-comprovantes
```