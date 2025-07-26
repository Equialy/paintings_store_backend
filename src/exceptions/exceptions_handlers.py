from aiohttp import ContentTypeError, request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from jose import JWTError
from pydantic import ValidationError

from src.exceptions.exception_base import (
    NotFoundError,
    BorrowLimitExceededError,
    NotValidPassword,
)


def register_exceptions_hanlder(app: FastAPI):
    @app.exception_handler(ValidationError)
    def handle_validation_error(request: Request, exc: ValidationError):
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"msg": "Unhandled Error", "detail": str(exc.errors())},
        )

    # @app.exception_handler(RequestValidationError)
    # def handle_request_validation_error(request: Request, exc: RequestValidationError):
    #     """Обработчик для ошибок Pydantic"""
    #     errors = []
    #     for error in exc.errors():
    #         field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
    #         msg = error["msg"]
    #         errors.append({"field": field, "message": msg})
    #
    #     return ORJSONResponse(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         content={"detail": "Validation error", "errors": errors, "body": exc.body},
    #     )

    @app.exception_handler(ValueError)
    async def handle_borrow_limit(request: Request, exc: ValueError):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
        )

    @app.exception_handler(BorrowLimitExceededError)
    async def handle_borrow_limit(request: Request, exc: BorrowLimitExceededError):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)}
        )

    @app.exception_handler(NoResultFound)
    def handle_not_found_row_db(request: Request, exc: NoResultFound):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg": "Not found", "detail": str(exc)},
        )

    @app.exception_handler(NotValidPassword)
    def handle_not_found_row_db(request: Request, exc: NotValidPassword):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"msg": "Пароли не совпадают", "detail": str(exc.msg)},
        )

    @app.exception_handler(JWTError)
    def handle_unauthorized_error(request: Request, exc: JWTError):
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"msg": "invalid token", "detail": str(exc)},
        )

    @app.exception_handler(IntegrityError)
    def handle_uniq_key_db(request: Request, exc: IntegrityError):
        error_msg = str(exc.orig)

        if "users_email_key" in error_msg:
            detail = "Email уже зарегистрирован"
        elif "users_username_key" in error_msg:
            detail = "Username уже занят"
        elif "quantity_non_negative" in error_msg:
            detail = f"{str(exc.orig).split("DETAIL")[1]}. Нет в наличии"
        elif "isbn" in error_msg:
            detail = "isbn уже существует"
        elif "duplicate key" in error_msg:
            detail = "Такой польозватель уже существует"
        else:
            detail = "Ошибка при сохранении в базу данных"
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"{detail}: {str(exc.params[0])}"},
        )

    @app.exception_handler(ContentTypeError)
    def handle_aiohttp_requests(request: Request, exc: ContentTypeError):

        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Wrong type JSON"},
        )

    @app.exception_handler(NotFoundError)
    def handle_not_found_error(request: Request, exc: NotFoundError):
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.msg}
        )
