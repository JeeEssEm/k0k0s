from database import AsyncSession
from core.s3_client import S3Client


class Repository:
    def __init__(self, session: AsyncSession, s3_client: S3Client):
        self.session = session
        self.s3_client = s3_client
