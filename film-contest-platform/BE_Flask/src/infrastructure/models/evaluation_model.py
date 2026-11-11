from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, UniqueConstraint
from datetime import datetime
from src.infrastructure.databases.base import Base

class EvaluationModel(Base):
    """
    Ánh xạ thực thể Đánh giá của Giám khảo (Evaluations - FE10):
    Phiếu đánh giá tổng hợp của giám khảo cho từng bài thi.
    Sau khi confirmed=True thì khóa sửa điểm (NFR-7).
    """
    __tablename__ = 'evaluations'
    __table_args__ = (
        UniqueConstraint('judge_id', 'submission_id', name='uq_judge_submission'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    judge_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    submission_id = Column(Integer, ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    comment = Column(Text, nullable=True)
    confirmed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'judge_id': self.judge_id,
            'submission_id': self.submission_id,
            'comment': self.comment,
            'confirmed': self.confirmed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
