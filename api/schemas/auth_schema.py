from pydantic import BaseModel, EmailStr, ConfigDict

class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    # token_type: str = "bearer"
