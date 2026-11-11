"""
Module: User Profile & Security (FastAPI)
Mục đích: Quản lý hồ sơ cá nhân, cập nhật thông tin cơ bản và đổi mật khẩu an toàn
Yêu cầu hệ thống: SRS: FR-1.4 | Task: CNPM-129 ([1.2] Hồ sơ cá nhân và bảo mật)
"""

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext

app = FastAPI(
    title="AI Film Photography Contest - Profile & Security Management",
    description="API Quản lý Hồ sơ cá nhân và Đổi mật khẩu (FR-1.4)",
    version="1.0.0"
)

# Cấu hình mã hóa mật khẩu (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Giả lập Database lưu trữ người dùng trong bộ nhớ tạm thời
fake_db_users = {
    "user@uth.edu.vn": {
        "id": 1,
        "full_name": "Nguyễn Văn A",
        "email": "user@uth.edu.vn",
        "phone": "0901234567",
        # Mật khẩu mặc định đã hash của chuỗi "123456"
        "hashed_password": pwd_context.hash("123456")
    }
}

# --- Schemas ---
class UserProfileUpdate(BaseModel):
    full_name: str = Field(..., example="Nguyễn Văn A")
    phone: str = Field(..., example="0901234567")

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., example="123456", description="Mật khẩu hiện tại")
    new_password: str = Field(..., example="NewPassword@123", description="Mật khẩu mới (Tối thiểu 6 ký tự)")

# --- Endpoints ---

@app.get("/api/v1/profile", tags=["User Profile"])
def get_user_profile(email: str = "user@uth.edu.vn"):
    """Xem thông tin cơ bản của hồ sơ cá nhân."""
    user = fake_db_users.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    
    return {
        "status": "success",
        "data": {
            "full_name": user["full_name"],
            "email": user["email"],
            "phone": user["phone"]
        }
    }

@app.put("/api/v1/profile", tags=["User Profile"])
def update_user_profile(profile_data: UserProfileUpdate, email: str = "user@uth.edu.vn"):
    """Sửa thông tin cơ bản của người dùng (Họ tên, số điện thoại)."""
    user = fake_db_users.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    
    user["full_name"] = profile_data.full_name
    user["phone"] = profile_data.phone
    
    return {
        "status": "success",
        "message": "Cập nhật thông tin cá nhân thành công!",
        "data": {
            "full_name": user["full_name"],
            "email": user["email"],
            "phone": user["phone"]
        }
    }

@app.put("/api/v1/auth/change-password", tags=["Security & Auth"])
def change_password(data: ChangePasswordRequest, email: str = "user@uth.edu.vn"):
    """Thực hiện đổi mật khẩu cho tài khoản người dùng đã đăng nhập."""
    user = fake_db_users.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    
    # 1. Kiểm tra mật khẩu cũ có chính xác không
    if not pwd_context.verify(data.old_password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu cũ không chính xác."
        )
    
    # 2. Kiểm tra độ dài/điều kiện mật khẩu mới (Ví dụ tối thiểu 6 ký tự)
    if len(data.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu mới phải có ít nhất 6 ký tự."
        )
        
    # 3. Mã hóa và lưu mật khẩu mới
    user["hashed_password"] = pwd_context.hash(data.new_password)
    
    return {
        "status": "success",
        "message": "Đổi mật khẩu thành công!"
    }
