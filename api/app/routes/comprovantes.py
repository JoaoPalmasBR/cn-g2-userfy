from fastapi import APIRouter
from app.utils.aws import s3
from app import config
from botocore.exceptions import ClientError

router = APIRouter()

@router.get("/comprovantes", tags=["Comprovantes"])
def listar_comprovantes():
    try:
        response = s3.list_objects_v2(Bucket=config.S3_BUCKET)
        print(response)
        arquivos = response.get("Contents", [])
        return [
            {
                "arquivo": obj["Key"],
                "url": f"http://localhost:4566/{config.S3_BUCKET}/{obj['Key']}"
            }
            for obj in arquivos
        ]
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            return []
        raise