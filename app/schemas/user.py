from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 5:
            raise ValueError("Senha deve conter no mínimo 5 caracteres")
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

