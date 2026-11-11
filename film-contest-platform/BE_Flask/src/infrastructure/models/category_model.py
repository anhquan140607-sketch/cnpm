from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class CategoryModel(Base):
    """
    Ánh xạ thực thể Hạng mục thi (Categories):
    Ảnh Đen Trắng, Ảnh Màu, Đường phố, kèm quy tắc số ảnh tối đa.
    """
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer, ForeignKey('contests.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(150), nullable=False)
    max_photos_per_participant = Column(Integer, nullable=False, default=5)
    submission_rules = Column(Text, nullable=True)
    award_structure = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'contest_id': self.contest_id,
            'name': self.name,
            'max_photos_per_participant': self.max_photos_per_participant,
            'submission_rules': self.submission_rules,
            'award_structure': self.award_structure,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
