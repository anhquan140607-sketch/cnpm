from flask import Blueprint, request, g
from src.services.auth_service import AuthService
from src.api.responses import success_response, error_response
from src.api.middleware import authenticate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Đăng ký tài khoản người tham gia (Participant)"""
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('name') or data.get('full_name')

    if not email or not password or not full_name:
        return error_response("Vui lòng cung cấp đầy đủ email, mật khẩu và họ tên", 400)

    try:
        result = auth_service.register(
            email=email,
            password=password,
            full_name=full_name,
            phone=data.get('phone'),
            bio=data.get('bio'),
            role=data.get('role', 'participant')
        )
        return success_response(result, "Đăng ký tài khoản thành công", 201)
    except Exception as e:
        status = getattr(e, 'status_code', 400)
        return error_response(str(e), status)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Đăng nhập hệ thống nhận JWT Access Token"""
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_response("Vui lòng cung cấp email và mật khẩu", 400)

    try:
        result = auth_service.login(email=email, password=password)
        return success_response(result, "Đăng nhập thành công")
    except Exception as e:
        status = getattr(e, 'status_code', 401)
        return error_response(str(e), status)

@auth_bp.route('/profile', methods=['GET'])
@authenticate_token
def get_profile():
    """Lấy thông tin người dùng đang đăng nhập"""
    user_id = g.user.get('id')
    user = auth_service.user_repo.get_by_id(user_id)
    if not user:
        return error_response("Không tìm thấy người dùng", 404)
    return success_response(user.to_dict(), "Lấy thông tin cá nhân thành công")
