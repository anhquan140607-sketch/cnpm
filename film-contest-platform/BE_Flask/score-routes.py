from flask import Blueprint, jsonify, request
from src.services.score_service import calculate_and_rank_submissions

score_bp = Blueprint('score_bp', __name__, url_prefix='/api/v1/scores')

@score_bp.route('/contests/<int:contest_id>/leaderboard', methods=['GET'])
def get_contest_leaderboard(contest_id):
    """
    API Controller Endpoint: GET /api/v1/scores/contests/<contest_id>/leaderboard
    Phục vụ Task CNPM-64: Trả về Bảng xếp hạng bài thi theo điểm số tự động
    """
    category_id = request.args.get('category_id', type=int)
    
    try:
        rankings = calculate_and_rank_submissions(contest_id, category_id)
        return jsonify({
            "status": "success",
            "contest_id": contest_id,
            "data": rankings
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500