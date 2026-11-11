import os
from src.infrastructure.databases.abstract_database import AbstractDatabase
from src.infrastructure.databases.base import Base

class DatabaseMySQL(AbstractDatabase):
    def __init__(self):
        uri = os.environ.get('MYSQL_DATABASE_URL') or 'mysql+pymysql://root:password@127.0.0.1:3306/film_contest_db'
        super().__init__(db_uri=uri)

    def init_database(self, app):
        Base.metadata.create_all(bind=self.engine)
        print("[MySQL] Connected successfully and synchronized ORM schema!")
