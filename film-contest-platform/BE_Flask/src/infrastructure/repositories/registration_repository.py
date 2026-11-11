from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.registration_model import RegistrationModel
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.contest_model import ContestModel
from src.infrastructure.models.category_model import CategoryModel

class RegistrationRepository:
    def __init__(self):
        self.db = FactoryDatabase.get_database()

    def create(self, reg: RegistrationModel):
        session = self.db.get_session()
        try:
            session.add(reg)
            session.commit()
            session.refresh(reg)
            return reg
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_by_contest(self, contest_id: int, status_filter: str = None):
        session = self.db.get_session()
        try:
            query = session.query(
                RegistrationModel.id,
                RegistrationModel.participant_id,
                UserModel.full_name.label('participant_name'),
                UserModel.email.label('participant_email'),
                RegistrationModel.contest_id,
                ContestModel.title.label('contest_title'),
                RegistrationModel.category_id,
                CategoryModel.name.label('category_name'),
                RegistrationModel.status,
                RegistrationModel.reason,
                RegistrationModel.created_at
            ).join(UserModel, RegistrationModel.participant_id == UserModel.id)\
             .join(ContestModel, RegistrationModel.contest_id == ContestModel.id)\
             .join(CategoryModel, RegistrationModel.category_id == CategoryModel.id)\
             .filter(RegistrationModel.contest_id == contest_id)

            if status_filter:
                query = query.filter(RegistrationModel.status == status_filter)

            results = query.order_by(RegistrationModel.created_at.desc()).all()
            return [dict(r._mapping) for r in results]
        finally:
            session.close()

    def review(self, reg_id: int, status: str, reason: str = None):
        session = self.db.get_session()
        try:
            reg = session.query(RegistrationModel).filter(RegistrationModel.id == reg_id).first()
            if not reg:
                return None
            reg.status = status
            if reason:
                reg.reason = reason
            session.commit()
            session.refresh(reg)
            return reg
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
