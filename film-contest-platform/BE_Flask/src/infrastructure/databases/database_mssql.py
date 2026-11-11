import os
from src.infrastructure.databases.abstract_database import AbstractDatabase
from src.infrastructure.databases.base import Base

class DatabaseMSSQL(AbstractDatabase):
    def __init__(self):
        uri = os.environ.get('MSSQL_DATABASE_URL') or 'mssql+pymssql://sa:password@127.0.0.1:1433/film_contest_db'
        super().__init__(db_uri=uri)

    def init_database(self, app):
        Base.metadata.create_all(bind=self.engine)
        print("[MS SQL Server] Connected successfully and synchronized ORM schema!")
