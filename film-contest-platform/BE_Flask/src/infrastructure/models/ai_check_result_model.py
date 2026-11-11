from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class AICheckResultModel(Base):
    """
    Ánh xạ thực thể Kết quả kiểm tra AI (AI Check Results - FE9):
    Kiểm tra tương đồng ảnh trùng lặp hoặc phát hiện ảnh AI.
    """
    __tablename__ = 'ai_check_results'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50), nullable=False)
    score = Column(Numeric(5, 4), nullable=False)
    matched_submission_id = Column(Integer, ForeignKey('submissions.id', ondelete='SET NULL'), nullable=True)
    decision = Column(String(50), nullable=False, default='pending')
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'submission_id': self.submission_id,
            'type': self.type,
            'score': float(self.score) if self.score else 0.0,
            'matched_submission_id': self.matched_submission_id,
            'decision': self.decision,
            'checked_at': self.checked_at.isoformat() if self.checked_at else None
        }
