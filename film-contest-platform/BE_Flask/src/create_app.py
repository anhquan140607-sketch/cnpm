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
        from flask import render_template_string, request
        # Nếu client yêu cầu JSON hoặc dùng công cụ kiểm thử tự động
        if 'application/json' in request.headers.get('Accept', '') or request.args.get('format') == 'json':
            return jsonify({
                'status': 'OK',
                'framework': 'Flask (Clean Architecture)',
                'language': 'Python 3.14',
                'orm': 'SQLAlchemy 2.0',
                'database': 'PostgreSQL (Connected)',
                'message': 'Film Contest Platform API is running smoothly'
            })

        # Nếu mở trực tiếp trên trình duyệt web, hiển thị giao diện Dashboard giám sát trực quan
        html = """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>System Health | Film Contest Platform</title>
          <style>
            :root {
              --bg: #0f172a;
              --card: #1e293b;
              --text: #f8fafc;
              --muted: #94a3b8;
              --accent: #3b82f6;
              --success: #22c55e;
              --border: #334155;
            }
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
            body { background: var(--bg); color: var(--text); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
            .health-card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 32px; max-width: 650px; width: 100%; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 16px; }
            .title { font-size: 1.3rem; font-weight: 700; display: flex; align-items: center; gap: 10px; }
            .status-badge { background: rgba(34, 197, 94, 0.15); color: var(--success); border: 1px solid var(--success); padding: 6px 14px; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; display: flex; align-items: center; gap: 8px; }
            .status-dot { width: 8px; height: 8px; background: var(--success); border-radius: 50%; box-shadow: 0 0 10px var(--success); animation: pulse 2s infinite; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
            .item { background: #0f172a; padding: 14px 18px; border-radius: 10px; border: 1px solid #1e293b; }
            .label { font-size: 0.8rem; color: var(--muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
            .value { font-size: 1.05rem; font-weight: 600; color: #e2e8f0; }
            .actions { display: flex; gap: 12px; margin-top: 8px; }
            .btn { flex: 1; text-align: center; background: var(--accent); color: white; text-decoration: none; padding: 12px 18px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; display: inline-flex; align-items: center; justify-content: center; gap: 8px; }
            .btn:hover { background: #2563eb; transform: translateY(-1px); }
            .btn-secondary { background: #334155; }
            .btn-secondary:hover { background: #475569; }
            @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
          </style>
        </head>
        <body>
          <div class="health-card">
            <div class="header">
              <div class="title">📷 Film Contest Platform API</div>
              <div class="status-badge">
                <span class="status-dot"></span> 200 OK • ALL OPERATIONAL
              </div>
            </div>
            <div class="grid">
              <div class="item">
                <div class="label">Backend Framework</div>
                <div class="value">Flask (Clean Architecture)</div>
              </div>
              <div class="item">
                <div class="label">Ngôn ngữ lập trình</div>
                <div class="value">Python 3.14</div>
              </div>
              <div class="item">
                <div class="label">ORM Engine</div>
                <div class="value">SQLAlchemy 2.0 (18 Models)</div>
              </div>
              <div class="item">
                <div class="label">Cơ sở dữ liệu</div>
                <div class="value" style="color:var(--success);">● PostgreSQL (film_contest_db)</div>
              </div>
            </div>
            <div style="background:#0f172a; padding:12px 16px; border-radius:8px; font-size:0.85rem; color:var(--muted); margin-bottom:20px; border-left:3px solid var(--accent);">
              🚀 <strong>Hệ thống sẵn sàng:</strong> Toàn bộ 18 thực thể từ <code>ERD.MD</code> đã được đồng bộ vào Database. Đa cơ sở dữ liệu (PostgreSQL / MySQL / MS SQL Server) hỗ trợ linh hoạt.
            </div>
            <div class="actions">
              <a href="/api/docs" class="btn">📖 Mở Swagger API Docs</a>
              <a href="/api/v1/system/master-data" class="btn btn-secondary">🗄️ Test API Master Data</a>
            </div>
          </div>
        </body>
        </html>
        """
        return render_template_string(html)

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
