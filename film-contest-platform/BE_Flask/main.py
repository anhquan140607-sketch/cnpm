"""
Module: Config Service
Mục đích: Quản lý đọc/ghi cấu hình hệ thống (Format ảnh, Dung lượng, Độ phân giải, Thông báo)
"""
import json
import os

CONFIG_FILE = "system_settings.json"

DEFAULT_SETTINGS = {
    "allowed_image_formats": ["jpg", "jpeg", "png", "webp"],
    "max_image_size_mb": 10.0,
    "min_image_resolution": {
        "width": 1920,
        "height": 1080
    },
    "enable_notifications": True
}

def get_settings() -> dict:
    """Đọc cấu hình hệ thống hiện tại từ file JSON hoặc trả về mặc định."""
    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings: dict) -> None:
    """Lưu cấu hình hệ thống mới vào file JSON."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)


"""
Module: Main Application (FastAPI)
Mục đích: Cung cấp API quản lý cấu hình hệ thống và API Validate Upload Ảnh cuộc thi
Yêu cầu hệ thống: SRS: FR-2.1 | Task: CNPM-117
"""

import io
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from pydantic import BaseModel, Field
from PIL import Image

from config_service import get_settings, save_settings

app = FastAPI(
    title="AI Film Photography Contest Management Platform",
    description="API Cấu hình hệ thống và Kiểm tra hợp lệ bài thi ảnh (FR-2.1)",
    version="1.0.0"
)

# --- Schemas ---
class ResolutionModel(BaseModel):
    width: int = Field(..., example=1920, description="Chiều rộng tối thiểu (px)")
    height: int = Field(..., example=1080, description="Chiều cao tối thiểu (px)")

class SystemSettingsSchema(BaseModel):
    allowed_image_formats: list[str] = Field(..., example=["jpg", "jpeg", "png", "webp"])
    max_image_size_mb: float = Field(..., example=10.0, description="Dung lượng tối đa (MB)")
    min_image_resolution: ResolutionModel
    enable_notifications: bool = Field(True, description="Trạng thái bật/tắt thông báo hệ thống")

# --- Endpoints Admin: Quản lý Cấu hình System ---
@app.get("/api/v1/admin/settings", response_model=dict, tags=["Admin Settings"])
def get_system_settings():
    """Lấy danh sách cấu hình hệ thống hiện tại."""
    return get_settings()

@app.put("/api/v1/admin/settings", tags=["Admin Settings"])
def update_system_settings(new_settings: SystemSettingsSchema):
    """Cập nhật cấu hình hệ thống (Dành cho Quản trị viên)."""
    save_settings(new_settings.dict())
    return {
        "status": "success",
        "message": "Cập nhật cấu hình hệ thống thành công!",
        "data": new_settings
    }

# --- Endpoint User: Submit Ảnh cuộc thi ---
@app.post("/api/v1/contests/submit-photo", tags=["Contest Submission"])
async def submit_contest_photo(file: UploadFile = File(...)):
    """
    Tải ảnh bài thi lên và tự động kiểm tra định dạng, dung lượng, độ phân giải
    dựa trên cấu hình hệ thống (SRS: FR-2.1).
    """
    settings = get_settings()
    
    # 1. Kiểm tra định dạng ảnh (File Extension)
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    allowed_formats = [fmt.lower() for fmt in settings["allowed_image_formats"]]
    
    if file_ext not in allowed_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Định dạng file '.{file_ext}' không hợp lệ. Hệ thống chỉ cho phép: {', '.join(allowed_formats)}"
        )
    
    # Đọc dữ liệu file vào bộ nhớ
    contents = await file.read()
    
    # 2. Kiểm tra dung lượng tối đa (Max File Size)
    file_size_mb = len(contents) / (1024 * 1024)
    max_size_mb = settings["max_image_size_mb"]
    if file_size_mb > max_size_mb:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dung lượng ảnh ({file_size_mb:.2f} MB) vượt quá giới hạn tối đa cho phép ({max_size_mb} MB)."
        )
        
    # 3. Kiểm tra độ phân giải / chất lượng ảnh (Min Resolution)
    try:
        image = Image.open(io.BytesIO(contents))
        width, height = image.size
        min_w = settings["min_image_resolution"]["width"]
        min_h = settings["min_image_resolution"]["height"]
        
        if width < min_w or height < min_h:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Độ phân giải ảnh quá thấp ({width}x{height}px). Yêu cầu tối thiểu là {min_w}x{min_h}px."
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File tải lên không phải là ảnh hợp lệ hoặc file bị lỗi."
        )

    # 4. Thiết lập thông báo hệ thống
    notification_msg = "Đã gửi thông báo xác nhận bài nộp." if settings["enable_notifications"] else "Hệ thống thông báo đang tắt."

    return {
        "status": "success",
        "message": "Ảnh hợp lệ và đã nộp thành công!",
        "details": {
            "filename": file.filename,
            "size_mb": round(file_size_mb, 2),
            "resolution": f"{width}x{height}px",
            "format": file_ext.upper(),
            "notification_status": notification_msg
        }
    }
