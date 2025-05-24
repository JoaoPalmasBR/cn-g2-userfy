#!/bin/sh

# Espera o LocalStack estar pronto
echo "Aguardando LocalStack..."
until curl -s http://localstack:4566/_localstack/health | grep "\"dynamodb\": \"running\"" > /dev/null; do
  sleep 2
done

echo "Criando tabela DynamoDB..."
aws --endpoint-url=http://localstack:4566 dynamodb create-table \
    --table-name Pedidos \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

echo "Criando fila SQS FIFO..."
aws --endpoint-url=http://localstack:4566 sqs create-queue \
    --queue-name pedidos.fifo \
    --attributes FifoQueue=true,ContentBasedDeduplication=true

echo "Criando bucket S3..."
aws --endpoint-url=http://localstack:4566 s3api create-bucket \
  --bucket foodz-comprovantes

echo "Recursos criados com sucesso!"
