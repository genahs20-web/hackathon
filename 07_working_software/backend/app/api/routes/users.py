"""Authentication endpoints (BR-1)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.user import (
    RefreshRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.api.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.config.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.models import Customer
from app.database.session import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)) -> UserResponse:
    if db.query(Customer).filter(Customer.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    customer = Customer(
        email=request.email,
        name=request.name,
        organization=request.organization,
        hashed_password=hash_password(request.password),
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return UserResponse.model_validate(customer)


@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    customer = db.query(Customer).filter(Customer.email == request.email).first()
    if customer is None or not verify_password(request.password, customer.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenResponse(
        access_token=create_access_token(customer.customer_id),
        refresh_token=create_refresh_token(customer.customer_id),
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/me", response_model=UserResponse)
def me(current_user: Customer = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest) -> TokenResponse:
    customer_id = decode_token(request.refresh_token, expected_type="refresh")
    return TokenResponse(
        access_token=create_access_token(customer_id), expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
