from uuid import uuid4

from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def test_user_model(db: AsyncSession):
    user = User(id=uuid4(), email="test@example.com", hashed_password="1234")
    db.add(user)
    await db.commit()
    assert user.id
