from flask import Blueprint, request, g
from src.services.contest_service import ContestService
from src.services.registration_service import RegistrationService
from src.api.responses import success_response, error_response
from src.api.middleware import authenticate_token, authorize_roles, optional_auth

contest_bp = Blueprint('contest', __name__, url_prefix='/api/v1/contests')
contest_service = ContestService()
reg_service = RegistrationService()

@contest_bp.route('', methods=['GET'])
@optional_auth
def list_contests():
    """Lấy danh sách cuộc thi có lọc trạng thái và phân trang"""
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    res = contest_service.list_contests(status, page, limit)
    return success_response(res['contests'], "Lấy danh sách cuộc thi thành công", 200, res['meta'])

@contest_bp.route('/<int:contest_id>', methods=['GET'])
@optional_auth
def get_contest(contest_id: int):
    """Chi tiết cuộc thi kèm các hạng mục và tiêu chí chấm"""
    try:
        details = contest_service.get_contest_details(contest_id)
        return success_response(details, "Lấy thông tin chi tiết cuộc thi thành công")
    except Exception as e:
        status = getattr(e, 'status_code', 404)
        return error_response(str(e), status)

@contest_bp.route('', methods=['POST'])
@authenticate_token
@authorize_roles('organizer', 'administrator')
def create_contest():
    """Organizer tạo mới cuộc thi"""
    data = request.get_json() or {}
    required = ['title', 'theme', 'submission_start', 'submission_end', 'judging_start', 'judging_end']
    for req in required:
        if not data.get(req):
            return error_response(f"Vui lòng cung cấp đầy đủ trường bắt buộc: {req}", 400)

    try:
        organizer_id = g.user.get('id', 2)
        created = contest_service.create_contest(organizer_id, data)
        return success_response(created, "Tạo cuộc thi thành công", 201)
    except Exception as e:
        status = getattr(e, 'status_code', 400)
        return error_response(str(e), status)

@contest_bp.route('/<int:contest_id>/categories', methods=['POST'])
@authenticate_token
@authorize_roles('organizer', 'administrator')
def add_category(contest_id: int):
    """Thêm hạng mục cho cuộc thi"""
    data = request.get_json() or {}
    if not data.get('name'):
        return error_response("Vui lòng cung cấp tên hạng mục thi", 400)

    try:
        organizer_id = g.user.get('id', 2)
        cat = contest_service.add_category(organizer_id, contest_id, data)
        return success_response(cat, "Thêm hạng mục thi thành công", 201)
    except Exception as e:
        status = getattr(e, 'status_code', 400)
        return error_response(str(e), status)

@contest_bp.route('/<int:contest_id>/criteria', methods=['POST'])
@authenticate_token
@authorize_roles('organizer', 'administrator')
def add_criterion(contest_id: int):
    """Thêm tiêu chí chấm cho cuộc thi (Tổng trọng số <= 100%)"""
    data = request.get_json() or {}
    if not data.get('name') or data.get('weight') is None:
        return error_response("Vui lòng cung cấp tên tiêu chí và trọng số (weight)", 400)

    try:
        organizer_id = g.user.get('id', 2)
        crit = contest_service.add_criterion(organizer_id, contest_id, data)
        return success_response(crit, "Thêm tiêu chí chấm thành công", 201)
    except Exception as e:
        status = getattr(e, 'status_code', 400)
        return error_response(str(e), status)

@contest_bp.route('/<int:contest_id>/registrations', methods=['GET'])
@optional_auth
def get_contest_registrations(contest_id: int):
    """Organizer xem danh sách thí sinh đăng ký tham gia (FE5 / CNPM-138)"""
    status = request.args.get('status')
    list_regs = reg_service.get_contest_registrations(contest_id, status)
    return success_response(list_regs, "Lấy danh sách đăng ký cuộc thi thành công")

@contest_bp.route('/registrations/<int:reg_id>/review', methods=['PUT'])
@optional_auth
def review_registration(reg_id: int):
    """Organizer duyệt hoặc từ chối đơn đăng ký (CNPM-138)"""
    data = request.get_json() or {}
    status = data.get('status')
    reason = data.get('reason')
    if not status:
        return error_response("Vui lòng cung cấp trạng thái duyệt (approved hoặc rejected)", 400)

    try:
        updated = reg_service.review_registration(reg_id, status, reason)
        return success_response(updated, f"Đã cập nhật trạng thái đơn đăng ký thành {status}")
    except Exception as e:
        status_code = getattr(e, 'status_code', 400)
        return error_response(str(e), status_code)
