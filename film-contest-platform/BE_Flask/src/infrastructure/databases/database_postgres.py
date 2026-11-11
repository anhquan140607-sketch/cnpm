import os
from src.infrastructure.databases.abstract_database import AbstractDatabase
from src.infrastructure.databases.base import Base

class DatabasePostgres(AbstractDatabase):
    def __init__(self):
        uri = os.environ.get('POSTGREE_DATABASE_URL') or 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/film_contest_db'
        if uri.startswith('postgresql://'):
            uri = uri.replace('postgresql://', 'postgresql+psycopg2://', 1)
        super().__init__(db_uri=uri)

    def init_database(self, app):
        Base.metadata.create_all(bind=self.engine)
        print("[PostgreSQL] Connected successfully and synchronized ORM schema!")
