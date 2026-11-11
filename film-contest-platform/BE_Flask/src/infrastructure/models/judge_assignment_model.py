from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from src.infrastructure.databases.base import Base

class JudgeAssignmentModel(Base):
    """
    Ánh xạ thực thể Phân công Giám khảo (Judge Assignments - FE10):
    Phân công ban giám khảo theo hạng mục thi và vòng thi.
    """
    __tablename__ = 'judge_assignments'
    __table_args__ = (
        UniqueConstraint('judge_id', 'category_id', 'round_id', name='uq_judge_cat_round'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    judge_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    round_id = Column(Integer, ForeignKey('rounds.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'judge_id': self.judge_id,
            'category_id': self.category_id,
            'round_id': self.round_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
