from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class ContestModel(Base):
    """
    Ánh xạ thực thể Cuộc thi (Contests) - Quản lý vòng đời trạng thái
    (draft -> open -> closed -> judging -> published -> archived) và khóa cấu hình.
    """
    __tablename__ = 'contests'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    theme = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    regulations = Column(Text, nullable=True)
    submission_start = Column(DateTime, nullable=False)
    submission_end = Column(DateTime, nullable=False)
    judging_start = Column(DateTime, nullable=False)
    judging_end = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default='draft')
    config_locked = Column(Boolean, nullable=False, default=False)
    created_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'theme': self.theme,
            'description': self.description,
            'regulations': self.regulations,
            'submission_start': self.submission_start.isoformat() if self.submission_start else None,
            'submission_end': self.submission_end.isoformat() if self.submission_end else None,
            'judging_start': self.judging_start.isoformat() if self.judging_start else None,
            'judging_end': self.judging_end.isoformat() if self.judging_end else None,
            'status': self.status,
            'config_locked': self.config_locked,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
