from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.contest_model import ContestModel
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.models.criterion_model import CriterionModel

class ContestRepository:
    def __init__(self):
        self.db = FactoryDatabase.get_database()

    def list_contests(self, status: str = None, page: int = 1, limit: int = 20):
        session = self.db.get_session()
        try:
            query = session.query(ContestModel)
            if status:
                query = query.filter(ContestModel.status == status)
            total = query.count()
            contests = query.order_by(ContestModel.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
            return contests, total
        finally:
            session.close()

    def get_by_id(self, contest_id: int):
        session = self.db.get_session()
        try:
            contest = session.query(ContestModel).filter(ContestModel.id == contest_id).first()
            if not contest:
                return None, [], []
            categories = session.query(CategoryModel).filter(CategoryModel.contest_id == contest_id).all()
            criteria = session.query(CriterionModel).filter(CriterionModel.contest_id == contest_id).all()
            return contest, categories, criteria
        finally:
            session.close()

    def create(self, contest: ContestModel):
        session = self.db.get_session()
        try:
            session.add(contest)
            session.commit()
            session.refresh(contest)
            return contest
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update(self, contest_id: int, data: dict):
        session = self.db.get_session()
        try:
            contest = session.query(ContestModel).filter(ContestModel.id == contest_id).first()
            if not contest:
                return None
            for key, val in data.items():
                if hasattr(contest, key) and val is not None:
                    setattr(contest, key, val)
            session.commit()
            session.refresh(contest)
            return contest
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add_category(self, category: CategoryModel):
        session = self.db.get_session()
        try:
            session.add(category)
            session.commit()
            session.refresh(category)
            return category
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def add_criterion(self, criterion: CriterionModel):
        session = self.db.get_session()
        try:
            session.add(criterion)
            session.commit()
            session.refresh(criterion)
            return criterion
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
