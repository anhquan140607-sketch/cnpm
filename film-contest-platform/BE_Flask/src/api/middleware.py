from functools import wraps
from flask import request, g
import jwt
import os
from datetime import datetime, timedelta
from src.api.responses import error_response

SECRET_KEY = os.environ.get('SECRET_KEY', 'film_contest_secret_key_jwt_2026')

def generate_token(user_id: int, email: str, role: str, expires_in_hours: int = 24) -> str:
    payload = {
        'id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def authenticate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response("Yêu cầu xác thực: Thiếu Access Token", 401, "UNAUTHORIZED")
        
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            g.user = payload
        except jwt.ExpiredSignatureError:
            return error_response("Token đã hết hạn", 401, "TOKEN_EXPIRED")
        except jwt.InvalidTokenError:
            return error_response("Token không hợp lệ", 403, "INVALID_TOKEN")
        
        return f(*args, **kwargs)
    return decorated

def authorize_roles(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(g, 'user', None)
            if not user:
                return error_response("Chưa đăng nhập", 401, "UNAUTHORIZED")
            if user.get('role') not in allowed_roles:
                return error_response(
                    f"Quyền truy cập bị từ chối. Vai trò '{user.get('role')}' không được phép thực hiện.",
                    403,
                    "FORBIDDEN"
                )
            return f(*args, **kwargs)
        return decorated
    return decorator

def optional_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                g.user = payload
            except:
                g.user = None
        else:
            g.user = None
        return f(*args, **kwargs)
    return decorated
