from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verify token and return user payload or raise 401 error."""
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
