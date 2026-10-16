import uuid
import pytest
from sqlalchemy import select

from backend.model.auth import Auth
from backend.schema.auth_schema import UserRegister
from backend.service.auth_service import AuthService

auth_service = AuthService()


@pytest.mark.asyncio
async def test_get_user_by_id(session):
    user_id = uuid.uuid4()
    database_user = Auth(
        id=user_id,
        email="newuser@email.com",
        password="hashed_password",
        username="newuser",
    )

    session.add(database_user)
    await session.commit()

    user = await auth_service.get_user_by_id(database_user.id, session)

    assert user is not None
    assert isinstance(user, Auth)
    assert user.id == user_id
    assert user.email == "newuser@email.com"
    assert user.username == "newuser"
    assert user.password == "hashed_password"


@pytest.mark.asyncio
async def test_get_user_by_email(session):
    user_id = uuid.uuid4()
    database_user = Auth(
        id=user_id,
        email="newuser@email.com",
        password="hashed_password",
        username="newuser",
    )

    session.add(database_user)
    await session.commit()

    user = await auth_service.get_user_by_email(database_user.email, session)

    assert user is not None
    assert isinstance(user, Auth)
    assert user.id == user_id
    assert user.email == "newuser@email.com"
    assert user.username == "newuser"
    assert user.password == "hashed_password"


@pytest.mark.asyncio
async def test_get_user_by_username(session):
    user_id = uuid.uuid4()
    database_user = Auth(
        id=user_id,
        email="newuser@email.com",
        password="hashed_password",
        username="newuser",
    )

    session.add(database_user)
    await session.commit()

    user = await auth_service.get_user_by_username(database_user.username, session)

    assert user is not None
    assert isinstance(user, Auth)
    assert user.id == user_id
    assert user.email == "newuser@email.com"
    assert user.username == "newuser"
    assert user.password == "hashed_password"


@pytest.mark.asyncio
async def test_create_user(session):
    user = UserRegister(
        email="newuser@email.com", password="non-hashed-password", username="newuser"
    )

    await auth_service.create_user(user, session)

    result = await session.execute(
        select(Auth).where(Auth.email == "newuser@email.com")
    )
    db_user = result.unique().scalar_one_or_none()

    # 3. Run your assertions against the database record
    assert db_user is not None
    assert db_user.email == "newuser@email.com"
    assert db_user.password != "non-hashed-password"
