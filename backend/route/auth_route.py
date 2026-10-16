from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import verify_password
from backend.error import InvalidUserCredential, UserAlreadyExists
from backend.external.database import get_session
from backend.schema.auth_schema import UserLogin, UserRegister
from backend.service.auth_service import AuthService

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserRegister, session: Annotated[AsyncSession, Depends(get_session)]
):
    # check email doesn't exist
    email_exist = await auth_service.get_user_by_email(user_data.email, session)
    username_exist = await auth_service.get_user_by_username(
        user_data.username, session
    )

    if email_exist or username_exist:
        raise UserAlreadyExists

    await auth_service.create_user(user_data, session)

    response = JSONResponse(content={"message": "User registered successfully"})

    return response


@auth_router.post("/signin")
async def login_user(
    user_data: UserLogin, session: Annotated[AsyncSession, Depends(get_session)]
):
    user_valid = None
    if user_data.email:
        user_valid = await auth_service.get_user_by_email(user_data.email, session)
    elif user_data.username:
        user_valid = await auth_service.get_user_by_username(
            user_data.username, session
        )

    if not user_valid or not verify_password(user_valid.password, user_data.password):
        raise InvalidUserCredential

    response = JSONResponse(content={"message": "Login successful"})

    return response
