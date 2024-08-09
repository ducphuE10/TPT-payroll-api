import base64
import boto3
from io import BytesIO
import uuid

from payroll.storage.schema import FileData

MINIO_URL = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET_NAME = "mybucket"

# Initialize MinIO (S3-compatible) client
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

# Ensure the bucket exists (create it if it doesn't)
try:
    s3_client.head_bucket(Bucket=MINIO_BUCKET_NAME)
except Exception:
    s3_client.create_bucket(Bucket=MINIO_BUCKET_NAME)


def upload_file_to_minio(
    file_content: bytes, filename: str, content_type: str
) -> FileData:
    try:
        file_id = str(uuid.uuid4())
        file_key = f"uploads/{file_id}/{filename}"

        if isinstance(file_content, str):
            raise ValueError("file_content should be a bytes-like object, not a string")

        # Upload the file to MinIO
        file_in_memory = BytesIO(file_content)
        s3_client.upload_fileobj(file_in_memory, MINIO_BUCKET_NAME, file_key)
        file_content_base64 = base64.b64encode(file_content).decode("utf-8")

        return FileData(
            filename=filename,
            content_type=content_type,
            file=file_content_base64,
            message="File upload successful.",
            path=file_key,
        )
    except Exception as e:
        return {
            "status": False,
            "error": str(e),
            "message": "File upload failed due to an internal error.",
        }
