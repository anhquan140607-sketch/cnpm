from flask import Blueprint, jsonify, request
from src.services.ai_check_service import update_ai_flag_decision

ai_bp = Blueprint('ai_bp', __name__, url_prefix='/api/v1/ai')

@ai_bp.route('/results/<int:res_id>/decision', methods=['PATCH'])
def ai_decision(res_id):
    """
    API PATCH /api/v1/ai/results/<res_id>/decision
    Cập nhật trạng thái duyệt cờ cảnh báo AI
    """
    data = request.json or {}
    decision = data.get('decision')
    res = update_ai_flag_decision(res_id, decision)
    return jsonify({"status": "success", "data": res}), 200
