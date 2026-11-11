class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class NotFoundException(AppException):
    def __init__(self, message: str = "Tài nguyên không tồn tại"):
        super().__init__(message, 404)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Yêu cầu xác thực tài khoản"):
        super().__init__(message, 401)

class ForbiddenException(AppException):
    def __init__(self, message: str = "Bạn không có quyền thực hiện hành động này"):
        super().__init__(message, 403)

class ValidationException(AppException):
    def __init__(self, message: str = "Dữ liệu yêu cầu không hợp lệ"):
        super().__init__(message, 422)
