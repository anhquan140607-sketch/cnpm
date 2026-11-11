from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.user_model import UserModel

class UserRepository:
    def __init__(self):
        self.db = FactoryDatabase.get_database()

    def get_by_id(self, user_id: int):
        session = self.db.get_session()
        try:
            return session.query(UserModel).filter(UserModel.id == user_id).first()
        finally:
            session.close()

    def get_by_email(self, email: str):
        session = self.db.get_session()
        try:
            return session.query(UserModel).filter(UserModel.email == email).first()
        finally:
            session.close()

    def create(self, user: UserModel):
        session = self.db.get_session()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
