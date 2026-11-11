from datetime import datetime
from src.models import db

class AICheckResult(db.Model):
    __tablename__ = 'ai_check_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'duplicate' hoặc 'ai_generated'
    score = db.Column(db.Numeric(5, 4), nullable=False)  # Điểm tương đồng / xác suất nghi vấn
    matched_submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id', ondelete='SET NULL'), nullable=True)
    decision = db.Column(db.String(50), nullable=False, default='pending')  # 'pending', 'flagged', 'cleared'
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
