from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from src.infrastructure.databases.base import Base

class RegistrationModel(Base):
    """
    Ánh xạ thực thể Đăng ký tham gia (Registrations):
    Quản lý đơn đăng ký thi của thí sinh và duyệt/từ chối từ Organizer (FE5).
    """
    __tablename__ = 'registrations'
    __table_args__ = (
        UniqueConstraint('participant_id', 'contest_id', 'category_id', name='uq_participant_contest_category'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    contest_id = Column(Integer, ForeignKey('contests.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    status = Column(String(50), nullable=False, default='pending')
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'contest_id': self.contest_id,
            'category_id': self.category_id,
            'status': self.status,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
