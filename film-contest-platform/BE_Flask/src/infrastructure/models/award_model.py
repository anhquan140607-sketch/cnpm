from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class AwardModel(Base):
    """
    Ánh xạ thực thể Giải thưởng cuộc thi (Awards - FE12):
    Giải Nhất, Giải Nhì, Giải Đặc biệt trao cho các tác phẩm xuất sắc.
    """
    __tablename__ = 'awards'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    submission_id = Column(Integer, ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(150), nullable=False)
    rank = Column(Integer, nullable=False)
    prize_amount = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'submission_id': self.submission_id,
            'title': self.title,
            'rank': self.rank,
            'prize_amount': self.prize_amount,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
