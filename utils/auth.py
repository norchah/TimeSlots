import logging
from datetime import datetime, timedelta

from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key-2025-timeslotru"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> dict:
    # Сначала пробуем cookie
    token_from_cookie = request.cookies.get("access_token")
    if token_from_cookie:
        logger.debug(f"Using token from cookie: {token_from_cookie[:10]}...")
        return verify_token(token_from_cookie)
    # Fallback на заголовок Authorization
    if token:
        logger.debug(f"Using token from Authorization header: {token[:10]}...")
        return verify_token(token)
    logger.warning("No token found in cookie or Authorization header")
    raise HTTPException(status_code=401, detail="Authentication required")


def set_jwt_cookie(response, token):
    """Устанавливает в куки токен(ы)"""
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Защита от XSS
        secure=True,  # Для localhost, в проде True
        samesite="none",  # Защита от CSRF
        max_age=30 * 60,  # 30 минут
        path="/",  # Доступна для всех маршрутов
        domain="localhost",
    )


def del_jwt_cookie(response):
    """Удаляет куки c токен(ы)"""
    response.delete_cookie(
        key="access_token",
        httponly=True,  # Защита от XSS
        secure=True,  # Для localhost, в проде True
        samesite="none",  # Защита от CSRF
        path="/",
        domain="localhost",
    )
