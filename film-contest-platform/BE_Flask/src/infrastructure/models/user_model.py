from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.infrastructure.databases.base import Base

class UserModel(Base):
    """
    Ánh xạ thực thể Người dùng (Users) - RBAC cho 4 vai trò:
    administrator, organizer, judge, participant.
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, default='participant')
    phone = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default='active')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'phone': self.phone,
            'bio': self.bio,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
