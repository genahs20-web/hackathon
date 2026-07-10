"""Pydantic schemas for authentication and user data."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=255)
    organization: str | None = Field(default=None, max_length=255)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, value: str) -> str:
        if not (any(c.isupper() for c in value) and any(c.islower() for c in value) and any(c.isdigit() for c in value)):
            raise ValueError("Password must contain upper, lower, and a digit")
        return value


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    customer_id: str
    email: EmailStr
    name: str
    organization: str | None
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
