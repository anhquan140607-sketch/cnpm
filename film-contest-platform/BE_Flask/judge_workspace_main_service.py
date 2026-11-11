"""
judge_workspace_main_service.py
Service xử lý không gian làm việc của giám khảo (Jira task CNPM-154 / [10.2]).
Bao gồm: danh sách bài được giao, xem ảnh phóng to, metadata phim và tiến độ chấm điểm.
"""

class JudgeWorkspaceMainService:
    def __init__(self, db_session=None):
        self.db = db_session

    def get_judge_dashboard(self, judge_id: int, contest_id: int, round_id: int):
        """
        [10.2] Lấy thông tin tổng quan không gian làm việc của giám khảo:
        - Danh sách bài được giao
        - Tiến độ chấm điểm (đã chấm / tổng số bài)
        """
        # Giả lập truy vấn dữ liệu từ DB
        assigned_submissions = [
            {
                "submission_id": 101,
                "title": "Hơi thở Sài Gòn",
                "image_url": "/uploads/images/saigon_breath.jpg",
                "metadata": {
                    "film_type": "35mm Color",
                    "camera": "Leica M6",
                    "lens": "50mm f/2",
                    "iso": 400,
                    "shutter_speed": "1/250s",
                    "aperture": "f/4"
                },
                "status": "graded", # graded / pending
                "score": 8.5
            },
            {
                "submission_id": 102,
                "title": "Mùa nước nổi",
                "image_url": "/uploads/images/flood_season.jpg",
                "metadata": {
                    "film_type": "120 Black & White",
                    "camera": "Hasselblad 500CM",
                    "lens": "80mm f/2.8",
                    "iso": 100,
                    "shutter_speed": "1/125s",
                    "aperture": "f/8"
                },
                "status": "pending",
                "score": None
            }
        ]

        total_assigned = len(assigned_submissions)
        total_graded = sum(1 for s in assigned_submissions if s["status"] == "graded")
        progress_percentage = (total_graded / total_assigned * 100) if total_assigned > 0 else 0

        return {
            "judge_id": judge_id,
            "contest_id": contest_id,
            "round_id": round_id,
            "progress": {
                "total_assigned": total_assigned,
                "total_graded": total_graded,
                "progress_percentage": progress_percentage
            },
            "submissions": assigned_submissions
        }

    def get_submission_detail_with_metadata(self, submission_id: int):
        """
        Lấy chi tiết bài thi để phóng to ảnh và xem đầy đủ thông số kỹ thuật (metadata phim).
        """
        # Giả lập trả về dữ liệu chi tiết
        return {
            "submission_id": submission_id,
            "image_zoom_url": f"/uploads/images/hires/submission_{submission_id}_zoom.jpg",
            "metadata": {
                "film_stock": "Kodak Portra 400",
                "development_process": "C-41",
                "camera_model": "Pentax K1000",
                "focal_length": "50mm",
                "exposure_info": "ISO 400, f/5.6, 1/500s",
                "photographer_notes": "Chụp tại chợ cũ vào buổi sáng sớm."
            }
        }
