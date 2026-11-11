"""
judge_workspace_service.py
Service xử lý không gian làm việc của Giám khảo và xác nhận khóa điểm thi (Jira task CNPM-156 / [10.5]).
"""

from datetime import datetime

class JudgeWorkspaceService:
    def __init__(self, db_session=None):
        self.db = db_session

    def get_assigned_submissions(self, judge_id: int, contest_id: int, round_id: int):
        """
        Lấy danh sách các bài thi được phân công cho giám khảo chấm trong một vòng thi.
        """
        # Logic truy vấn DB để lấy bài thi & điểm số hiện tại
        return {
            "judge_id": judge_id,
            "contest_id": contest_id,
            "round_id": round_id,
            "submissions": []
        }

    def save_draft_score(self, judge_id: int, submission_id: int, score: float, feedback: str = ""):
        """
        Lưu điểm tạm (nháp). Chưa khóa điểm, giám khảo vẫn có thể chỉnh sửa.
        """
        # Kiểm tra xem điểm đã bị khóa trước đó chưa
        is_locked = False # Giả định kiểm tra từ DB
        if is_locked:
            raise ValueError("Kết quả đã được xác nhận và bị khóa. Không thể sửa đổi điểm.")

        return {
            "status": "success",
            "message": "Đã lưu điểm nháp thành công.",
            "submission_id": submission_id,
            "score": score,
            "is_locked": False
        }

    def confirm_final_results(self, judge_id: int, contest_id: int, round_id: int):
        """
        [10.5] Xác nhận kết quả cuối của giám khảo:
        Giám khảo xác nhận nộp kết quả chấm điểm. 
        Sau khi xác nhận, toàn bộ điểm số của giám khảo trong vòng thi này sẽ bị KHOÁ (is_locked = True).
        """
        confirmation_time = datetime.now().isoformat()
        
        # Cập nhật trạng thái trong Database:
        # UPDATE judge_evaluations SET is_locked = True, confirmed_at = confirmation_time 
        # WHERE judge_id = judge_id AND round_id = round_id
        
        return {
            "status": "success",
            "message": "Xác nhận kết quả thành công. Tất cả điểm số đã được khóa.",
            "judge_id": judge_id,
            "contest_id": contest_id,
            "round_id": round_id,
            "is_locked": True,
            "confirmed_at": confirmation_time
        }

    def check_score_lock_status(self, judge_id: int, round_id: int):
        """
        Kiểm tra xem giám khảo đã khóa điểm ở vòng thi này chưa.
        """
        # Trả về trạng thái khóa điểm
        return {
            "judge_id": judge_id,
            "round_id": round_id,
            "is_locked": True
        }
