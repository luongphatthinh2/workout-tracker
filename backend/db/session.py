# db/session.py
from typing import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session_factory = request.app.container.session_factory()
    async with session_factory() as session:
        yield session
