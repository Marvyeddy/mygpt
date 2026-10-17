from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from backend.core.config import config as cfg
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security import (
    create_refresh_token,
    create_session_token,
    verify_password,
)
from backend.error import InvalidUserCredential, UserAlreadyExists
from backend.external.database import get_session
from backend.external.email import send_email
from backend.schema.auth_schema import UserLogin, UserRegister
from backend.service.auth_service import AuthService

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(
    bg: BackgroundTasks,
    user_data: UserRegister,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    # check email doesn't exist
    email_exist = await auth_service.get_user_by_email(user_data.email, session)
    username_exist = await auth_service.get_user_by_username(
        user_data.username, session
    )

    if email_exist or username_exist:
        raise UserAlreadyExists

    new_user = await auth_service.create_user(user_data, session)

    bg.add_task(
        send_email,
        subject="Welcome to Velmio! ✨",
        recipients=[new_user.email],
        template_name="welcome.html",
        context={
            "first_name": new_user.username,
            "app_url": cfg.FRONTEND_URL,
        },
    )

    # send tokens for authorization

    token_dict = {"sub": str(new_user.id), "email": new_user.email}

    session_token = create_session_token(token_dict)
    refresh_token = create_refresh_token(token_dict)

    response = JSONResponse(
        content={
            "message": "User registered successfully",
            "session_token": session_token,
            "refresh_token": refresh_token,
        },
        status_code=status.HTTP_201_CREATED,
    )

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60,  # 1 hour
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 2,  # 2 days
        path="/",
    )

    return response


@auth_router.post("/signin")
async def login_user(
    user_data: UserLogin, session: Annotated[AsyncSession, Depends(get_session)]
):
    valid_user = None
    if user_data.email:
        valid_user = await auth_service.get_user_by_email(user_data.email, session)
    elif user_data.username:
        valid_user = await auth_service.get_user_by_username(
            user_data.username, session
        )

    if not valid_user or not verify_password(valid_user.password, user_data.password):
        raise InvalidUserCredential

    # send tokens for authorization

    token_dict = {"sub": str(valid_user.id), "email": valid_user.email}

    session_token = create_session_token(token_dict)
    refresh_token = create_refresh_token(token_dict)

    response = JSONResponse(
        content={
            "message": "Login successful",
            "session_token": session_token,
            "refresh_token": refresh_token,
        }
    )

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=60 * 60,
        path="/",
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=60 * 60 * 24 * 2,
        path="/",
        secure=True,
        samesite="lax",
    )

    return response
