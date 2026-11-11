import os
import base64
import time
from flask import Blueprint, request, g, send_from_directory
from src.services.registration_service import RegistrationService
from src.api.responses import success_response, error_response
from src.api.middleware import optional_auth

participant_bp = Blueprint('participant', __name__, url_prefix='/api/v1/participant')
reg_service = RegistrationService()

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@participant_bp.route('/registrations', methods=['POST'])
@optional_auth
def register_contest():
    """Thí sinh đăng ký tham gia cuộc thi (FE5 / CNPM-44)"""
    data = request.get_json() or {}
    contest_id = data.get('contest_id')
    category_id = data.get('category_id')

    if not contest_id or not category_id:
        return error_response("Vui lòng cung cấp contest_id và category_id", 400)

    participant_id = g.user.get('id') if g.user else 4  # Default fallback participant (id=4)
    try:
        res = reg_service.register_contest(participant_id, contest_id, category_id)
        return success_response(res, "Đăng ký tham gia cuộc thi thành công", 201)
    except Exception as e:
        return error_response(str(e), 400)

@participant_bp.route('/upload', methods=['POST'])
@optional_auth
def upload_photo():
    """Thí sinh upload ảnh scan cuộn phim (FE7 / CNPM-48 / CNPM-141)"""
    data = request.get_json() or {}
    image_data = data.get('image_data')
    filename = data.get('filename', 'scan.jpg')

    if not image_data:
        return error_response("Vui lòng cung cấp dữ liệu hình ảnh (base64 image_data)", 400)

    try:
        # Tách header base64 nếu có
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        binary_data = base64.b64decode(image_data)
        saved_name = f"scan-{int(time.time() * 1000)}-{filename}"
        file_path = os.path.join(UPLOAD_DIR, saved_name)

        with open(file_path, 'wb') as f:
            f.write(binary_data)

        user_id = g.user.get('id') if g.user else 4
        result = {
            'url': f"http://localhost:5000/uploads/{saved_name}",
            'filename': saved_name,
            'size': len(binary_data),
            'uploaded_by': user_id
        }
        return success_response(result, "Upload ảnh lên máy chủ lưu trữ thành công", 201)
    except Exception as e:
        return error_response(f"Lỗi khi xử lý file ảnh: {str(e)}", 400)
