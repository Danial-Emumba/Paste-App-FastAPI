from datetime import datetime, timedelta
from typing import Union
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.config.settings import settings
from app.db.models.user import User
from app.db.repository import get_user_by_username, create_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(username: str, password: str) -> Union[User, bool]:
    user = get_user_by_username(username)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError("Invalid token")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def create_user(user: User) -> User:
    try:
        return create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current logged-in user object from the JWT token.

    Args:
        token (str): The JWT token provided in the request header.

    Returns:
        User: The User object representing the current logged-in user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")