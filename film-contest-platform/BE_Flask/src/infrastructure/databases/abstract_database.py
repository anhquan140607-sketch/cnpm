from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class AbstractDatabase(ABC):
    def __init__(self, db_uri: str = None):
        if not db_uri:
            db_uri = os.environ.get('POSTGREE_DATABASE_URL') or 'postgresql://postgres:postgres@127.0.0.1:5432/film_contest_db'
        self.database_uri = db_uri
        self.engine = create_engine(self.database_uri, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = self.SessionLocal()

    @abstractmethod
    def init_database(self, app):
        pass

    def get_session(self):
        return self.SessionLocal()
