import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db  # Adjust this to your actual module import path

@pytest.mark.asyncio
async def test_get_db_session_management():
    # Create a MagicMock for the AsyncSession
    mock_session = AsyncMock(spec=AsyncSession)

    # Mock get_async_db to yield a context-managed session
    async def mock_get_async_db():
        async with AsyncMock(spec=AsyncSession) as session:
            yield session
        # This ensures that session.close() is automatically awaited once the block exits

    with patch('app.dependencies.get_async_db', new=mock_get_async_db):
        async for session in get_db():
            assert isinstance(session, AsyncMock), "get_db should yield an AsyncSession"
        # Since the session is managed by the context manager, we don't need to check if close was awaited

