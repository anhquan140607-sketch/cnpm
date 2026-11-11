from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class RefreshTokenModel(Base):
    """
    Ánh xạ thực thể Token làm mới (Refresh Tokens - FE1):
    Hỗ trợ cơ chế bảo mật phiên đăng nhập JWT và Refresh Token Rotation.
    """
    __tablename__ = 'refresh_tokens'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(Text, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
