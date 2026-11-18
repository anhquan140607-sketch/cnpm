from datetime import datetime
from src.models import db, Contest, Submission, Award
from src.services.notification_service import NotificationService

class ResultService:
    @staticmethod
    def publish_official_results(contest_id, admin_id):
        """CNPM-73 [12.1]: Công bố kết quả chính thức"""
        contest = Contest.query.get(contest_id)
        if not contest or contest.status != 'evaluating':
            return {"success": False, "message": "Cuộc thi không tồn tại hoặc chưa kết thúc chấm điểm"}
            
        contest.status = 'completed'
        contest.ended_at = datetime.utcnow()
        db.session.commit()
        
        # CNPM-91 & CNPM-96: Trigger thông báo kết quả
        NotificationService.notify_contest_completed(contest)
        return {"success": True, "message": "Công bố kết quả thành công"}

    @staticmethod
    def assign_award(submission_id, award_name, rank, prize_amount=None):
        """CNPM-74 [12.2]: Ghi nhận giải thưởng"""
        submission = Submission.query.get(submission_id)
        if not submission:
            return {"success": False, "message": "Bài thi không tồn tại"}
            
        new_award = Award(
            submission_id=submission_id,
            category_id=submission.category_id,
            title=award_name,
            rank=rank,
            prize_amount=prize_amount
        )
        db.session.add(new_award)
        db.session.commit()
        
        # CNPM-91 & CNPM-96: Trigger thông báo đạt giải
        NotificationService.notify_award_winner(submission, new_award)
        return {"success": True, "data": {"award_id": new_award.id, "title": new_award.title}}
