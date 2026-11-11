from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, JSON
from datetime import datetime
from src.infrastructure.databases.base import Base

class ArchiveItemModel(Base):
    """
    Ánh xạ thực thể Lưu trữ số (Archive Items - FE13):
    Lưu trữ tác phẩm xuất sắc sau khi kết thúc cuộc thi kèm bản chụp metadata.
    """
    __tablename__ = 'archive_items'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey('submissions.id', ondelete='CASCADE'), nullable=False)
    metadata_snapshot = Column(JSON, nullable=False)
    judging_comments = Column(Text, nullable=True)
    archived_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'submission_id': self.submission_id,
            'metadata_snapshot': self.metadata_snapshot,
            'judging_comments': self.judging_comments,
            'archived_at': self.archived_at.isoformat() if self.archived_at else None
        }
