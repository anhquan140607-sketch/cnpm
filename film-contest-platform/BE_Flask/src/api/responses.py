from flask import jsonify

def success_response(data=None, message: str = "Thành công", status_code: int = 200, meta: dict = None):
    res = {
        'success': True,
        'message': message,
        'data': data
    }
    if meta:
        res['meta'] = meta
    return jsonify(res), status_code

def error_response(message: str = "Đã xảy ra lỗi", status_code: int = 400, code: str = None):
    if not code:
        code = 'BAD_REQUEST' if status_code == 400 else 'ERROR'
    res = {
        'success': False,
        'error': {
            'code': code,
            'message': message
        }
    }
    return jsonify(res), status_code
