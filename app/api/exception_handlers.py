from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import AlreadyRegisteredUser, InvalidUserEmail, InvalidUserPassword

def register_exception_handlers(app):

    @app.exception_handler(AlreadyRegisteredUser)
    async def handler_already_registered_user(request: Request, exc: AlreadyRegisteredUser):
        return JSONResponse(status_code=409, content={"detail": str(exc)})
    
    @app.exception_handler(InvalidUserPassword)
    async def handler_invalid_user_password(request: Request, exc: InvalidUserPassword):
        return JSONResponse(status_code=400, content={"detail": str(exc)})
    
    @app.exception_handler(InvalidUserEmail)
    async def handler_invalid_user_email(request: Request, exc: InvalidUserEmail):
        return JSONResponse(status_code=404, content={"detail": str(exc)})