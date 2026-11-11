from flask import Blueprint, request, jsonify
from src.services.auth_service import register_user, login_user

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    user_id = register_user(data.get('username'), data.get('email'), data.get('password'))
    return jsonify({"status": "success", "user_id": user_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    token = login_user(data.get('email'), data.get('password'))
    if token:
        return jsonify({"status": "success", "token": token}), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401
