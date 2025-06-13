import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "Users")
SQS_QUEUE = os.getenv("SQS_QUEUE", "users.fifo")
