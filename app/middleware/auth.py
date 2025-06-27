from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.users.dependencies import get_access_token, get_current_user
from app.users.models import User


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        try:
            token = get_access_token(request)
            user = await get_current_user(token)
            request.state.user = user
        except Exception:
            pass
        response = await call_next(request)
        return response