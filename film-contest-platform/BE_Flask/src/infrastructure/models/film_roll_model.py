from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from src.infrastructure.databases.base import Base

class FilmRollModel(Base):
    """
    Ánh xạ thực thể Cuộn phim (Film Rolls - FE6):
    Minh chứng nguồn gốc cuộn phim vật lý chụp ảnh thi của thí sinh.
    """
    __tablename__ = 'film_rolls'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    film_brand_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    film_stock_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    iso_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    film_format_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    camera_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    lens_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    lab_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    scanner_id = Column(Integer, ForeignKey('master_data.id', ondelete='SET NULL'), nullable=True)
    scan_specs = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'participant_id': self.participant_id,
            'film_brand_id': self.film_brand_id,
            'film_stock_id': self.film_stock_id,
            'iso_id': self.iso_id,
            'film_format_id': self.film_format_id,
            'camera_id': self.camera_id,
            'lens_id': self.lens_id,
            'lab_id': self.lab_id,
            'scanner_id': self.scanner_id,
            'scan_specs': self.scan_specs,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
