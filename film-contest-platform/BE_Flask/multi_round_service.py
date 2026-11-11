"""
Module: Multi-Round Judging System (FastAPI)
Mục đích: Quản lý cấu hình nhiều vòng chấm thi (Ví dụ: Vòng loại/Shortlist và Vòng chung kết), 
          cùng cơ chế chọn lọc bài thi đi tiếp vào vòng sau.
Yêu cầu hệ thống: SRS: FR-10.4 | Task: CNPM-72 ([10.4] Nhiều vòng chấm)
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="AI Film Photography Contest - Multi-Round Judging Platform",
    description="API Quản lý nhiều vòng chấm và chọn bài vào vòng sau (FR-10.4)",
    version="1.0.0"
)

# --- Giả lập cơ sở dữ liệu lưu trữ vòng thi và bài thi ---
fake_rounds_db = {
    1: {"round_id": 1, "round_name": "Vòng Sơ khảo (Shortlist)", "status": "Active"},
    2: {"round_id": 2, "round_name": "Vòng Chung kết", "status": "Pending"}
}

fake_submissions_db = [
    {"submission_id": "SUB-001", "title": "Hơi thở Sài Gòn", "current_round": 1, "score": 8.5, "status": "In Review"},
    {"submission_id": "SUB-002", "title": "Hoài niệm cũ", "current_round": 1, "score": 9.2, "status": "In Review"},
    {"submission_id": "SUB-003", "title": "Đêm phố thị", "current_round": 1, "score": 6.0, "status": "In Review"},
]

# --- Schemas ---
class RoundConfig(BaseModel):
    round_id: int
    round_name: str
    status: str

class PromoteSubmissionsRequest(BaseModel):
    submission_ids: List[str] = Field(..., description="Danh sách mã bài thi được chọn vào vòng sau")
    target_round_id: int = Field(..., description="Mã vòng thi tiếp theo (Ví dụ: Vòng chung kết)")

# --- Endpoints ---

@app.get("/api/v1/admin/rounds", tags=["Multi-Round Management"])
def get_contest_rounds():
    """Lấy danh sách các vòng chấm thi hiện tại (Ví dụ: Shortlist, Chung kết)."""
    return {
        "status": "success",
        "data": list(fake_rounds_db.values())
    }

@app.get("/api/v1/admin/rounds/{round_id}/submissions", tags=["Multi-Round Management"])
def get_submissions_by_round(round_id: int):
    """Lấy danh sách bài thi thuộc một vòng chấm cụ thể."""
    filtered = [sub for sub in fake_submissions_db if sub["current_round"] == round_id]
    return {
        "status": "success",
        "round_id": round_id,
        "total": len(filtered),
        "data": filtered
    }

@app.post("/api/v1/admin/rounds/promote", tags=["Multi-Round Management"])
def promote_submissions_to_next_round(data: PromoteSubmissionsRequest):
    """
    Chọn lọc bài thi từ vòng hiện tại đi tiếp vào vòng sau (SRS: FR-10.4).
    """
    if data.target_round_id not in fake_rounds_db:
        raise HTTPException(status_code=404, detail="Vòng thi đích không tồn tại trong hệ thống.")
    
    promoted_count = 0
    for sub in fake_submissions_db:
        if sub["submission_id"] in data.submission_ids:
            sub["current_round"] = data.target_round_id
            sub["status"] = f"Promoted to Round {data.target_round_id}"
            promoted_count += 1
            
    return {
        "status": "success",
        "message": f"Đã chuyển thành công {promoted_count} bài thi vào vòng tiếp theo!",
        "target_round": fake_rounds_db[data.target_round_id]["round_name"]
    }
