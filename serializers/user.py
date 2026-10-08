# serializers/user.py

from pydantic import BaseModel


# Form Validations
class UserRegistrationSchema(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


# Response Schemas
class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str

    model_config = {
    "from_attributes": True
}


class UserTokenSchema(BaseModel):
    token: str
    message: str