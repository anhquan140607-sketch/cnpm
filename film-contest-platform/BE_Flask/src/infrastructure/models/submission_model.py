from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class SubmissionModel(Base):
    """
    Ánh xạ thực thể Tác phẩm dự thi (Submissions - FE7):
    Liên kết trực tiếp Frame gốc, Hạng mục và Thí sinh.
    """
    __tablename__ = 'submissions'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(Integer, ForeignKey('frames.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    participant_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_path = Column(String(500), nullable=False)
    thumbnail_path = Column(String(500), nullable=True)
    negative_ref_path = Column(String(500), nullable=True)
    status = Column(String(50), nullable=False, default='submitted')
    keywords = Column(String(500), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'frame_id': self.frame_id,
            'category_id': self.category_id,
            'participant_id': self.participant_id,
            'title': self.title,
            'description': self.description,
            'image_path': self.image_path,
            'thumbnail_path': self.thumbnail_path,
            'negative_ref_path': self.negative_ref_path,
            'status': self.status,
            'keywords': self.keywords,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }
