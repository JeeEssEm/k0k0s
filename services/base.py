from fastapi import Depends

from database import AsyncSession, get_session


class Service:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        annotations = self.__class__.__annotations__
        self.repository = annotations['repository'](session)
        if annotations.get('s3_repository'):
            self.s3_repository = annotations['s3_repository']()
