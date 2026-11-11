from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from src.infrastructure.databases.base import Base

class MasterDataModel(Base):
    """
    Ánh xạ thực thể Dữ liệu danh mục chuẩn hóa (Master Data - FE2):
    film_brand, film_stock, iso, film_format, camera, lens, lab, scanner.
    """
    __tablename__ = 'master_data'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    value = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default='active')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'value': self.value,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
