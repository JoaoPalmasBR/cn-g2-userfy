#!/bin/sh

echo "🔄 Esperando LocalStack na porta 4566..."

until nc -z localstack 4566; do
  echo "⌛ LocalStack ainda não disponível..."
  sleep 2
done

echo "✅ LocalStack acessível. Iniciando aplicação..."
exec "$@"
