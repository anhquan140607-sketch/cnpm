from sqlalchemy.orm import declarative_base

# Base class cho toàn bộ SQLAlchemy ORM Models
# Ánh xạ các class Python (Entities) -> Tables trong Database
Base = declarative_base()
