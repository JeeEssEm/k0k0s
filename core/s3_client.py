from contextlib import asynccontextmanager
from io import BytesIO

from aiobotocore.session import get_session

from config import settings


# class Bucket(Enum):
#     user_images: str = 'user_images'
#     item_images: str = 'item_images'


class S3Client:
    def __init__(self):
        self.config = {
            'aws_access_key_id': settings.S3_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.S3_SECRET_ACCESS_KEY,
            'endpoint_url': settings.S3_ENDPOINT,
        }
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as s3_client:
            yield s3_client

    async def upload_file(self, file_name: str, bucket: str, file: BytesIO):
        async with self.get_client() as s3_client:
            await s3_client.put_object(
                Bucket=bucket,
                Key=file_name,
                Body=file,
            )

    async def get_file(self, file_name: str, bucket: str):
        async with self.get_client() as s3_client:
            resp = await s3_client.get_object(Bucket=bucket, Key=file_name)
            return BytesIO(await resp['Body'].read())


def get_s3_client():
    return S3Client()
