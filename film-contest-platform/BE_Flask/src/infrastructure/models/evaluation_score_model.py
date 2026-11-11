from sqlalchemy import Column, Integer, Numeric, ForeignKey, UniqueConstraint
from src.infrastructure.databases.base import Base

class EvaluationScoreModel(Base):
    """
    Ánh xạ thực thể Chi tiết Điểm số theo Tiêu chí (Evaluation Scores - FE10):
    Lưu điểm chi tiết cho từng tiêu chí chấm thi.
    """
    __tablename__ = 'evaluation_scores'
    __table_args__ = (
        UniqueConstraint('evaluation_id', 'criterion_id', name='uq_eval_criterion'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    evaluation_id = Column(Integer, ForeignKey('evaluations.id', ondelete='CASCADE'), nullable=False)
    criterion_id = Column(Integer, ForeignKey('criteria.id', ondelete='CASCADE'), nullable=False)
    score = Column(Numeric(5, 2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'evaluation_id': self.evaluation_id,
            'criterion_id': self.criterion_id,
            'score': float(self.score) if self.score else 0.0
        }
