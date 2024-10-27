from fastapi import Depends

from core.s3_client import S3Client, get_s3_client
from database import AsyncSession, get_session


class Service:
    def __init__(self, session: AsyncSession = Depends(get_session),
                 s3_client: S3Client = Depends(get_s3_client)
                 ) -> None:
        self.repository = self.__class__.__annotations__['repository'](
            session, s3_client
        )
