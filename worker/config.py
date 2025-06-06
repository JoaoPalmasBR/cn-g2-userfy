import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "Pedidos")
SQS_QUEUE = os.getenv("SQS_QUEUE", "pedidos.fifo")
S3_BUCKET = os.getenv("S3_BUCKET", "foodz-comprovantes")
