import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from src.infrastructure.databases import init_db
from src.api.controllers.auth_controller import auth_bp
from src.api.controllers.contest_controller import contest_bp
from src.api.controllers.master_data_controller import master_data_bp
from src.api.controllers.participant_controller import participant_bp
from src.api.responses import error_response
from src.domain.exceptions import AppException

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 1. Đăng ký các Blueprints (Controllers)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contest_bp)
    app.register_blueprint(master_data_bp)
    app.register_blueprint(participant_bp)

    # 2. Phục vụ thư mục upload ảnh tĩnh
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(upload_dir, filename)

    # 3. Route kiểm tra trạng thái sức khỏe (Health check)
    @app.route('/health')
    @app.route('/api/v1/health')
    def health_check():
        return jsonify({
            'status': 'OK',
            'framework': 'Flask (Clean Architecture)',
            'language': 'Python 3.14',
            'orm': 'SQLAlchemy 2.0',
            'message': 'Film Contest Platform API is running'
        })

    # 4. Tích hợp Swagger UI tại /api/docs
    SWAGGER_URL = '/api/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Film Photography Contest API (Flask Clean Architecture)"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/swagger.json')
    def swagger_json():
        swagger_spec = {
            "swagger": "2.0",
            "info": {
                "title": "Film Photography Contest Platform API (Python Flask)",
                "description": "REST API theo chuẩn Clean Architecture & SQLAlchemy ORM mapping 18 thực thể từ ERD.MD",
                "version": "1.0.0"
            },
            "basePath": "/api/v1",
            "schemes": ["http"],
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Nhập token với định dạng: Bearer <access_token>"
                }
            },
            "paths": {
                "/auth/login": {
                    "post": {
                        "tags": ["1. Xác thực & Tài khoản (FE1)"],
                        "summary": "Đăng nhập nhận Access Token",
                        "parameters": [{
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string", "example": "participant@filmcontest.vn"},
                                    "password": {"type": "string", "example": "password123"}
                                }
                            }
                        }],
                        "responses": {"200": {"description": "Thành công"}}
                    }
                },
                "/auth/register": {
                    "post": {
                        "tags": ["1. Xác thực & Tài khoản (FE1)"],
                        "summary": "Đăng ký tài khoản thí sinh",
                        "parameters": [{
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "example": "Nguyễn Văn A"},
                                    "email": {"type": "string", "example": "nguyenvana@gmail.com"},
                                    "password": {"type": "string", "example": "password123"}
                                }
                            }
                        }],
                        "responses": {"201": {"description": "Tạo thành công"}}
                    }
                },
                "/system/master-data": {
                    "get": {
                        "tags": ["2. Hệ thống & Danh mục (FE2)"],
                        "summary": "Xem danh mục Master Data chuẩn hóa (film_brand, film_stock, iso, camera, scanner...)",
                        "parameters": [{
                            "name": "type",
                            "in": "query",
                            "type": "string",
                            "enum": ["film_brand", "film_stock", "iso", "film_format", "camera", "lens", "lab", "scanner"]
                        }],
                        "responses": {"200": {"description": "Thành công"}}
                    }
                },
                "/contests": {
                    "get": {
                        "tags": ["3. Cuộc thi & Hạng mục (FE3, FE4)"],
                        "summary": "Lấy danh sách cuộc thi",
                        "responses": {"200": {"description": "Thành công"}}
                    },
                    "post": {
                        "tags": ["3. Cuộc thi & Hạng mục (FE3, FE4)"],
                        "summary": "Organizer tạo mới cuộc thi",
                        "security": [{"Bearer": []}],
                        "parameters": [{
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "example": "Hà Nội - Những khung hình thời gian 2026"},
                                    "theme": {"type": "string", "example": "Nhiếp ảnh phim đường phố"},
                                    "submission_start": {"type": "string", "example": "2026-11-01T00:00:00Z"},
                                    "submission_end": {"type": "string", "example": "2026-11-20T23:59:59Z"},
                                    "judging_start": {"type": "string", "example": "2026-11-21T00:00:00Z"},
                                    "judging_end": {"type": "string", "example": "2026-11-30T23:59:59Z"}
                                }
                            }
                        }],
                        "responses": {"201": {"description": "Tạo thành công"}}
                    }
                },
                "/contests/{id}/registrations": {
                    "get": {
                        "tags": ["4. Ban tổ chức - Duyệt đăng ký (FE5 / CNPM-138)"],
                        "summary": "Organizer xem danh sách đơn đăng ký",
                        "parameters": [{"name": "id", "in": "path", "required": True, "type": "integer"}],
                        "responses": {"200": {"description": "Thành công"}}
                    }
                },
                "/contests/registrations/{reg_id}/review": {
                    "put": {
                        "tags": ["4. Ban tổ chức - Duyệt đăng ký (FE5 / CNPM-138)"],
                        "summary": "Organizer duyệt hoặc từ chối đơn đăng ký (approved/rejected)",
                        "parameters": [
                            {"name": "reg_id", "in": "path", "required": True, "type": "integer"},
                            {
                                "name": "body",
                                "in": "body",
                                "required": True,
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "enum": ["approved", "rejected"], "example": "approved"},
                                        "reason": {"type": "string", "example": "Đủ điều kiện thể lệ và cuộn phim hợp lệ"}
                                    }
                                }
                            }
                        ],
                        "responses": {"200": {"description": "Thành công"}}
                    }
                },
                "/participant/registrations": {
                    "post": {
                        "tags": ["5. Thí sinh - Đăng ký & Nộp ảnh (FE5, FE7)"],
                        "summary": "Thí sinh đăng ký tham gia cuộc thi (CNPM-44)",
                        "parameters": [{
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "contest_id": {"type": "integer", "example": 1},
                                    "category_id": {"type": "integer", "example": 1}
                                }
                            }
                        }],
                        "responses": {"201": {"description": "Thành công"}}
                    }
                },
                "/participant/upload": {
                    "post": {
                        "tags": ["5. Thí sinh - Đăng ký & Nộp ảnh (FE5, FE7)"],
                        "summary": "Thí sinh upload ảnh scan cuộn phim (CNPM-48 / CNPM-141)",
                        "parameters": [{
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "filename": {"type": "string", "example": "film-scan-hanoi.jpg"},
                                    "image_data": {"type": "string", "example": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////"}
                                }
                            }
                        }],
                        "responses": {"201": {"description": "Upload thành công"}}
                    }
                }
            }
        }
        return jsonify(swagger_spec)

    # 5. Khởi tạo kết nối CSDL và mapping ORM
    try:
        init_db(app)
    except Exception as e:
        print(f"[DB Warning] Could not initialize DB: {e}")

    # 6. Global Error Handler
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return error_response(error.message, error.status_code)

    @app.errorhandler(404)
    def handle_404(error):
        return error_response("Endpoint không tồn tại trên hệ thống", 404, "NOT_FOUND")

    @app.errorhandler(500)
    def handle_500(error):
        return error_response("Lỗi máy chủ nội bộ", 500, "INTERNAL_SERVER_ERROR")

    return app
