from flask import Blueprint, request
from src.services.master_data_service import MasterDataService
from src.api.responses import success_response, error_response
from src.api.middleware import authenticate_token, authorize_roles

master_data_bp = Blueprint('master_data', __name__, url_prefix='/api/v1/system/master-data')
master_data_service = MasterDataService()

@master_data_bp.route('', methods=['GET'])
def get_master_data():
    """Lấy danh mục dữ liệu dùng chung (film_brand, film_stock, iso, camera, lens, lab, scanner) - FE2"""
    type_filter = request.args.get('type')
    items = master_data_service.get_all(type_filter)
    return success_response(items, "Lấy danh mục master data thành công")

@master_data_bp.route('', methods=['POST'])
@authenticate_token
@authorize_roles('administrator')
def create_master_data():
    """Administrator thêm mục danh mục mới"""
    data = request.get_json() or {}
    if not data.get('type') or not data.get('value'):
        return error_response("Vui lòng cung cấp type và value", 400)

    try:
        created = master_data_service.create(data)
        return success_response(created, "Thêm danh mục master data thành công", 201)
    except Exception as e:
        return error_response(str(e), 400)
