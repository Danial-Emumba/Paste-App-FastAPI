from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.api.services.auth_service import decode_access_token

class AuthMiddleware:
    def __init__(self, oauth2_scheme: OAuth2PasswordBearer):
        self.oauth2_scheme = oauth2_scheme

    async def __call__(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
        try:
            payload = decode_access_token(token)
            request.state.user = payload["sub"]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        response = await call_next(request)
        return response
