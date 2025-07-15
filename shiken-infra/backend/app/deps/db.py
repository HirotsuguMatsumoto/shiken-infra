from typing import Annotated

from app.db import async_session_maker
from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession


async def get_async_session():
    async with async_session_maker() as session:
        yield session
        await session.close()


CurrentAsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
