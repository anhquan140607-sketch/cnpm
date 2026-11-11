"""
Module: Judge Workspace System (FastAPI)
Mục đích: Xây dựng API quản lý Không gian làm việc của giám khảo (Danh sách bài được giao, phóng to ảnh, xem metadata phim, tiến độ chấm).
Yêu cầu hệ thống: SRS: FR-10.2 | Task: CNPM-61 ([10.2] Không gian làm việc của giám khảo)
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="AI Film Photography Contest - Judge Workspace",
    description="API Không gian làm việc của giám khảo (FR-10.2)",
    version="1.0.0"
)

# --- Giả lập cơ sở dữ liệu bài thi được giao cho giám khảo ---
fake_judge_assignments = {
    "judge_01@uth.edu.vn": [
        {
            "submission_id": "SUB-101",
            "title": "Hơi thở Sài Gòn thập niên 90",
            "image_url": "https://example.com/images/sub101.jpg",
            "film_metadata": {
                "camera": "Leica M6",
                "film_stock": "Kodak Portra 400",
                "lens": "Summicron 35mm f/2",
                "iso": 400,
                "shutter_speed": "1/250s",
                "aperture": "f/4"
            },
            "status": "Pending", # Pending, In Progress, Completed
            "score": None
        },
        {
            "submission_id": "SUB-102",
            "title": "Khoảng lặng ven sông",
            "image_url": "https://example.com/images/sub102.jpg",
            "film_metadata": {
                "camera": "Canon AE-1",
                "film_stock": "Fujifilm C200",
                "lens": "FD 50mm f/1.8",
                "iso": 200,
                "shutter_speed": "1/500s",
                "aperture": "f/2.8"
            },
            "status": "Completed",
            "score": 9.0
        }
    ]
}

class ScoreSubmissionRequest(BaseModel):
    score: float = Field(..., ge=0, le=10, description="Điểm số bài thi (0 - 10)")
    feedback: Optional[str] = Field(None, description="Nhận xét của giám khảo")

# --- Endpoints ---

@app.get("/api/v1/judge/workspace", tags=["Judge Workspace"])
def get_judge_workspace(judge_email: str = "judge_01@uth.edu.vn"):
    """
    Lấy danh sách bài thi được giao và tiến độ chấm của giám khảo (SRS: FR-10.2).
    """
    assignments = fake_judge_assignments.get(judge_email, [])
    
    total_assigned = len(assignments)
    completed = len([sub for sub in assignments if sub["status"] == "Completed"])
    progress_percentage = (completed / total_assigned * 100) if total_assigned > 0 else 0
    
    return {
        "status": "success",
        "progress_summary": {
            "total_assigned": total_assigned,
            "completed": completed,
            "pending": total_assigned - completed,
            "progress_percentage": round(progress_percentage, 2)
        },
        "assigned_submissions": assignments
    }

@app.get("/api/v1/judge/submissions/{submission_id}/detail", tags=["Judge Workspace"])
def get_submission_detail_for_judge(submission_id: str, judge_email: str = "judge_01@uth.edu.vn"):
    """
    Xem chi tiết bài thi, hỗ trợ phóng to ảnh và xem thông tin metadata phim (FR-10.2).
    """
    assignments = fake_judge_assignments.get(judge_email, [])
    target = next((sub for sub in assignments if sub["submission_id"] == submission_id), None)
    
    if not target:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài thi hoặc bạn không được phân công chấm bài này.")
        
    return {
        "status": "success",
        "data": {
            "submission_id": target["submission_id"],
            "title": target["title"],
            "high_res_image_url": target["image_url"], # Dùng cho tính năng phóng to ảnh
            "film_metadata": target["film_metadata"],  # Metadata phim kỹ thuật
            "current_status": target["status"],
            "score": target["score"]
        }
    }

@app.post("/api/v1/judge/submissions/{submission_id}/score", tags=["Judge Workspace"])
def submit_score_and_review(submission_id: str, data: ScoreSubmissionRequest, judge_email: str = "judge_01@uth.edu.vn"):
    """
    Giám khảo chấm điểm và cập nhật tiến độ hoàn thành bài thi.
    """
    assignments = fake_judge_assignments.get(judge_email, [])
    target = next((sub for sub in assignments if sub["submission_id"] == submission_id), None)
    
    if not target:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài thi được giao.")
        
    target["score"] = data.score
    target["status"] = "Completed"
    
    return {
        "status": "success",
        "message": f"Đã chấm điểm thành công cho bài thi {submission_id}!",
        "updated_submission": target
    }
