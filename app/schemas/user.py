from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email: str
    password: str

