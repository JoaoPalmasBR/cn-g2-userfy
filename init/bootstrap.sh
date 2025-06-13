#!/bin/sh
# Espera o LocalStack estar pronto
echo "Aguardando LocalStack..."
until curl -s http://localstack:4566/_localstack/health | grep "\"dynamodb\": \"running\"" > /dev/null; do
  sleep 2
done
echo "Criando tabela DynamoDB..."
aws --endpoint-url=http://localstack:4566 dynamodb create-table \
    --table-name Users \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
echo "Criando fila SQS FIFO..."
aws --endpoint-url=http://localstack:4566 sqs create-queue \
    --queue-name users.fifo \
    --attributes FifoQueue=true,ContentBasedDeduplication=true
echo "Recursos criados com sucesso!"