from fastapi import Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    AlreadyRegisteredUser,
    AlreadyRegisteredVehicle,
    InvalidUserEmail,
    InvalidUserPassword,
    NotRegisteredVehicle,
    QueryIdNotFound,
    UserEmailNotFound,
    UserIdNotFound,
)


def register_exception_handlers(app):

    @app.exception_handler(AlreadyRegisteredUser)
    async def handler_already_registered_user(request: Request, exc: AlreadyRegisteredUser):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
    
    @app.exception_handler(InvalidUserPassword)
    async def handler_invalid_user_password(request: Request, exc: InvalidUserPassword):
        return JSONResponse(status_code=401, content={"detail": str(exc)})
    
    @app.exception_handler(InvalidUserEmail)
    async def handler_invalid_user_email(request: Request, exc: InvalidUserEmail):
        return JSONResponse(status_code=401, content={"detail": str(exc)})
    
    @app.exception_handler(NotRegisteredVehicle)
    async def handler_not_registered_vehicle(request: Request, exc: NotRegisteredVehicle):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    
    @app.exception_handler(AlreadyRegisteredVehicle)
    async def handler_already_registered_vehicle(request: Request, exc: AlreadyRegisteredVehicle):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
    
    @app.exception_handler(UserEmailNotFound)
    async def handler_user_email_not_found(request: Request, exc: UserEmailNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    
    @app.exception_handler(UserIdNotFound)
    async def handler_user_id_not_found(request: Request, exc: UserIdNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})
    
    @app.exception_handler(QueryIdNotFound)
    async def handler_query_id_not_found(request: Request, exc: QueryIdNotFound):
        return JSONResponse(status_code=404, content={"detail": str(exc)})