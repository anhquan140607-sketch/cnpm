from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from src.infrastructure.databases.base import Base

class FrameModel(Base):
    """
    Ánh xạ thực thể Khung hình (Frames - FE6):
    Từng ô khung hình cụ thể (Frame 0-38) trong cuộn phim vật lý.
    """
    __tablename__ = 'frames'
    __table_args__ = (
        UniqueConstraint('film_roll_id', 'frame_number', name='uq_roll_frame'),
        {'extend_existing': True}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    film_roll_id = Column(Integer, ForeignKey('film_rolls.id', ondelete='CASCADE'), nullable=False)
    frame_number = Column(Integer, nullable=False)
    shooting_location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'film_roll_id': self.film_roll_id,
            'frame_number': self.frame_number,
            'shooting_location': self.shooting_location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
