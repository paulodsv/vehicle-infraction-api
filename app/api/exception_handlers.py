from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import AlreadyRegisteredUser

def register_exception_handlers(app):

    @app.exception_handler(AlreadyRegisteredUser)
    async def handler_already_registered_user(request: Request, exc: AlreadyRegisteredUser):
        return JSONResponse(status_code=409, content={"detail": str(exc)})