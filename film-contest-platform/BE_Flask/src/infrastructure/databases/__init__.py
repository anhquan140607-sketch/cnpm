from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.databases.base import Base

def init_db(app):
    """Khởi tạo kết nối CSDL và đồng bộ ORM mapping."""
    db = FactoryDatabase.get_database()
    db.init_database(app)
    return db
