"""
Multi-Round Service Module
Jira Task: CNPM-165 [10.4] Nhiều vòng chấm
Description: Quản lý cấu hình nhiều vòng chấm (Shortlist, Chung kết) và chuyển bài thi vào vòng sau.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class MultiRoundService:
    def __init__(self, db_session=None):
        """
        Khởi tạo service quản lý các vòng chấm thi.
        :param db_session: Phiên làm việc với Database (nếu sử dụng SQLAlchemy hoặc ORM khác)
        """
        self.db = db_session

    def create_contest_round(
        self, 
        contest_id: str, 
        round_name: str, 
        round_order: int, 
        min_score_pass: float = 0.0,
        max_submissions_pass: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Tạo một vòng chấm mới cho cuộc thi (VD: Vòng sơ khảo, Vòng shortlist, Vòng chung kết).
        """
        new_round = {
            "contest_id": contest_id,
            "round_name": round_name,
            "round_order": round_order,
            "min_score_pass": min_score_pass,
            "max_submissions_pass": max_submissions_pass,
            "status": "pending",  # pending, active, completed
            "created_at": datetime.utcnow()
        }
        
        # TODO: Lưu new_round vào Database
        return {
            "success": True,
            "message": f"Đã tạo thành công vòng '{round_name}' (Thứ tự: {round_order}).",
            "data": new_round
        }

    def get_submissions_in_round(self, round_id: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách bài thi và tổng điểm hiện tại trong một vòng thi cụ thể.
        """
        # TODO: TRUY VẤN DATABASE để lấy danh sách bài thi kèm điểm số trung bình của vòng này
        submissions = [
            {"submission_id": "sub_01", "title": "Bình minh trên biển", "avg_score": 8.5, "status": "scored"},
            {"submission_id": "sub_02", "title": "Phố cổ Hà Nội", "avg_score": 9.2, "status": "scored"},
            {"submission_id": "sub_03", "title": "Mùa thu Tây Bắc", "avg_score": 6.8, "status": "scored"},
        ]
        return submissions

    def filter_and_promote_submissions(
        self, 
        current_round_id: str, 
        next_round_id: str, 
        passing_limit: Optional[int] = None,
        min_score: float = 0.0
    ) -> Dict[str, Any]:
        """
        Tự động lọc bài thi đạt yêu cầu ở vòng hiện tại và chuyển (promote) sang vòng tiếp theo.
        """
        # 1. Lấy tất cả bài thi ở vòng hiện tại
        all_submissions = self.get_submissions_in_round(current_round_id)

        # 2. Lọc các bài thi có điểm lớn hơn hoặc bằng min_score
        qualified_submissions = [
            sub for sub in all_submissions if sub.get("avg_score", 0) >= min_score
        ]

        # 3. Sắp xếp danh sách theo điểm từ cao xuống thấp
        qualified_submissions.sort(key=lambda x: x.get("avg_score", 0), reverse=True)

        # 4. Nếu có giới hạn số lượng bài thi lọt vào vòng trong (Shortlist)
        if passing_limit and passing_limit > 0:
            promoted_list = qualified_submissions[:passing_limit]
        else:
            promoted_list = qualified_submissions

        promoted_ids = [sub["submission_id"] for sub in promoted_list]

        # TODO: Cập nhật CSDL - Thêm các bài thi có ID trong promoted_ids vào next_round_id
        # và đánh dấu chuyển vòng thành công.

        return {
            "success": True,
            "current_round_id": current_round_id,
            "next_round_id": next_round_id,
            "total_promoted": len(promoted_ids),
            "promoted_submission_ids": promoted_ids
        }

    def update_round_status(self, round_id: str, status: str) -> Dict[str, Any]:
        """
        Cập nhật trạng thái vòng thi (ví dụ: 'active' để bắt đầu chấm, 'completed' để kết thúc).
        """
        valid_statuses = ["pending", "active", "completed"]
        if status not in valid_statuses:
            return {"success": False, "message": "Trạng thái không hợp lệ."}

        # TODO: Cập nhật status vào DB cho round_id
        return {
            "success": True,
            "round_id": round_id,
            "new_status": status,
            "message": f"Đã cập nhật trạng thái vòng thi thành '{status}'."
        }


# --- Ví dụ cách gọi và thử nghiệm service ---
if __name__ == "__main__":
    service = MultiRoundService()

    # 1. Tạo 2 vòng thi
    service.create_contest_round(contest_id="contest_01", round_name="Vòng Sơ Khảo", round_order=1)
    service.create_contest_round(contest_id="contest_01", round_name="Vòng Chung Kết", round_order=2)

    # 2. Chuyển top 2 bài có điểm >= 8.0 từ vòng 1 sang vòng 2
    result = service.filter_and_promote_submissions(
        current_round_id="round_1",
        next_round_id="round_2",
        passing_limit=2,
        min_score=8.0
    )
    print("Kết quả chuyển vòng:", result)