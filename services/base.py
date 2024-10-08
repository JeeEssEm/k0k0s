from fastapi import Depends

from database import AsyncSession, get_session


class Service:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.repository = self.__class__.__annotations__['repository'](session)
