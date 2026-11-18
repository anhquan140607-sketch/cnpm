from src.models import db, Notification, User
import logging

class NotificationService:
    @staticmethod
    def send_in_app_notification(user_id, title, content, notif_type="info"):
        """CNPM-96 [16.2]: Thông báo trong ứng dụng"""
        notif = Notification(
            user_id=user_id,
            title=title,
            content=content,
            type=notif_type,
            is_read=False
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def send_email(to_email, subject, body):
        """CNPM-91 [16.1]: Thông báo qua email"""
        # Integration point for SMTP / SendGrid
        logging.info(f"EMAIL SENT TO {to_email} | Subject: {subject} | Body: {body}")
        return True

    @classmethod
    def notify_award_winner(cls, submission, award):
        """Thông báo trúng giải"""
        user = User.query.get(submission.author_id)
        title = "Chúc mừng! Tác phẩm của bạn đã đoạt giải"
        content = f"Tác phẩm '{submission.title}' đạt '{award.title}'."
        
        cls.send_in_app_notification(user.id, title, content, "award")
        cls.send_email(user.email, title, content)
        
    @classmethod
    def notify_contest_completed(cls, contest):
        """Thông báo cuộc thi kết thúc"""
        logging.info(f"Contest {contest.id} completed. Notifying all participants.")
