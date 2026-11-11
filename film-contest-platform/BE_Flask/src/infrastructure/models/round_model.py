from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class RoundModel(Base):
    """
    Ánh xạ thực thể Vòng thi (Rounds): Vòng sơ khảo, Vòng chung khảo.
    """
    __tablename__ = 'rounds'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer, ForeignKey('contests.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    sequence = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'contest_id': self.contest_id,
            'name': self.name,
            'sequence': self.sequence,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
