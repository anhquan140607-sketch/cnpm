from functools import wraps
from flask import Blueprint, jsonify, request
from src.services.sprint3_120_115_service import verify_submission_manually, check_user_has_role

bp_120_115 = Blueprint('bp_120_115', __name__, url_prefix='/api/v1')

# CNPM-115: Decorator Phân quyền RBAC Middleware
def require_roles(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = request.headers.get('X-User-Id')
            if not user_id or not check_user_has_role(int(user_id), roles):
                return jsonify({"status": "error", "message": "Forbidden: Insufficient privileges"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# CNPM-120: Endpoint duyệt bài thủ công cho Organizer/Admin
@bp_120_115.route('/submissions/<int:sub_id>/verify-manual', methods=['POST'])
@require_roles('organizer', 'admin')
def manual_verify(sub_id):
    data = request.json or {}
    reviewer_id = int(request.headers.get('X-User-Id', 0))
    res = verify_submission_manually(sub_id, reviewer_id, data.get('status'), data.get('reason'))
    return jsonify({"status": "success", "data": res}), 200
