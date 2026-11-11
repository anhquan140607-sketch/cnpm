from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class CriterionModel(Base):
    """
    Ánh xạ thực thể Tiêu chí chấm điểm (Criteria):
    Ràng buộc tổng trọng số của một cuộc thi = 100%.
    """
    __tablename__ = 'criteria'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer, ForeignKey('contests.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    weight = Column(Numeric(5, 2), nullable=False)
    max_score = Column(Numeric(5, 2), nullable=False, default=10.00)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'contest_id': self.contest_id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'weight': float(self.weight) if self.weight else 0.0,
            'max_score': float(self.max_score) if self.max_score else 10.0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
