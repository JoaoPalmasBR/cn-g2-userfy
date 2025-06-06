import boto3
from app import config

session = boto3.Session(
    aws_access_key_id="joao",
    aws_secret_access_key="joao",
    region_name=config.AWS_REGION
)

dynamodb = session.resource("dynamodb", endpoint_url="http://localstack:4566")
sqs = session.client("sqs", endpoint_url="http://localstack:4566")
# aws.py
s3 = session.client("s3", endpoint_url="http://localstack:4566")
sns = session.client("sns", endpoint_url="http://localstack:4566")