from typing import Any, Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class MyGPTException(Exception):
    """The root error exception class"""


def create_exception_handler(
    status_code: int, detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    def exception_handler(request: Request, exc: MyGPTException):
        return JSONResponse(status_code=status_code, content=detail)

    return exception_handler


def require_error(app: FastAPI):
    @app.exception_handler(500)
    async def server_exception(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Oops! something went wrong",
                "error_code": "server_error",
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception(request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Oops! something went wrong",
                "error_code": "database_error",
            },
        )
