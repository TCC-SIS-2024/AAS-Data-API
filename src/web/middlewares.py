from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from src.web.http_helper import HttpHelper
from src.web.dependencies import jwt_encoder
from fastapi.responses import JSONResponse


class CheckTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.headers.get('Authorization')

        if token is not None:
            jwt_access = token.split(' ')[1]
            try:
                encoder = jwt_encoder()
                encoder.decode_jwt(jwt_access)
            except jwt.ExpiredSignatureError:
                http_custom_response = HttpHelper.unauthorized(Exception('Token is expired'))
                return JSONResponse(status_code=http_custom_response.status_code, content=http_custom_response.model_dump())
            except jwt.InvalidTokenError:
                http_custom_response = HttpHelper.unauthorized(Exception('Token is invalid'))
                return JSONResponse(status_code=http_custom_response.status_code, content=http_custom_response.model_dump())
        response = await call_next(request)
        return response

class CheckRoleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.headers.get('Authorization')

        if token is not None:
            jwt_access = token.split(' ')[1]
            try:
                encoder = jwt_encoder()
                decoded_jwt = encoder.decode_jwt(jwt_access)
                permissions = decoded_jwt.get('permissions')
                role = decoded_jwt.get('role')

                request.state.__setattr__('role', role)
                request.state.__setattr__('permissions', permissions)

            except jwt.ExpiredSignatureError:
                http_custom_response = HttpHelper.unauthorized(Exception('Token is expired'))
                return JSONResponse(status_code=http_custom_response.status_code,
                                    content=http_custom_response.model_dump())
            except jwt.InvalidTokenError:
                http_custom_response = HttpHelper.unauthorized(Exception('Token is invalid'))
                return JSONResponse(status_code=http_custom_response.status_code,
                                    content=http_custom_response.model_dump())
        response = await call_next(request)
        return response