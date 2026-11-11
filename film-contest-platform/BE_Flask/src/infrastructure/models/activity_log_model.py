from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime
from src.infrastructure.databases.base import Base

class ActivityLogModel(Base):
    """
    Ánh xạ thực thể Nhật ký kiểm toán (Activity Logs - NFR-7):
    Ghi nhận dấu vết hoạt động của người dùng cho mục đích kiểm soát hệ thống.
    """
    __tablename__ = 'activity_logs'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
