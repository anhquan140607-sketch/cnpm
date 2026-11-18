from flask import Blueprint, request, jsonify
from src.services.result_service import ResultService
from src.middlewares.auth_middleware import admin_required

result_bp = Blueprint('result_routes', __name__, url_prefix='/api/v1/results')

@result_bp.route('/publish/<int:contest_id>', methods=['POST'])
@admin_required
def publish_results(contest_id):
    """CNPM-73: API Công bố kết quả"""
    admin_id = request.user.id 
    res = ResultService.publish_official_results(contest_id, admin_id)
    return jsonify(res), 200 if res["success"] else 400

@result_bp.route('/award', methods=['POST'])
@admin_required
def assign_award():
    """CNPM-74: API Trao giải"""
    data = request.json
    res = ResultService.assign_award(
        submission_id=data['submission_id'],
        award_name=data['award_name'],
        rank=data['rank'],
        prize_amount=data.get('prize_amount')
    )
    return jsonify(res), 201 if res["success"] else 400
