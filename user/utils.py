from datetime import datetime, timedelta
from typing import Any, Union

from core.dependencies import get_db
from fastapi import HTTPException, Request, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "c87201cd0ea515c359feb1baf8dd9099c2ea4083020ac5b9212c0de0e7551d1d"  # generated using openssl rand -hex 32

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

security = HTTPBearer()


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
#
#
# def get_current_user(
#     request: Request, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     from crud import user
#
#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM, options={"verify_aud": False})
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user_in_db = user.get_user_by_username(session, username)
#     if user_in_db is None:
#         raise credentials_exception
#     return user_in_db


def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    from user.crud import user

    try:
        token = authorization.credentials
        payload = jwt.decode(token, key=JWT_SECRET_KEY,
                             options={"verify_signature": False, "verify_aud": False, "verify_iss": False})
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_in_db = user.get_user_by_username(session, username)
    if user_in_db is None:
        raise credentials_exception
    return user_in_db
