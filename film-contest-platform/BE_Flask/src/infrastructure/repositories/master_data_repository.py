from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.master_data_model import MasterDataModel

class MasterDataRepository:
    def __init__(self):
        self.db = FactoryDatabase.get_database()

    def get_all(self, type_filter: str = None, active_only: bool = True):
        session = self.db.get_session()
        try:
            query = session.query(MasterDataModel)
            if type_filter:
                query = query.filter(MasterDataModel.type == type_filter)
            if active_only:
                query = query.filter(MasterDataModel.status == 'active')
            return query.order_by(MasterDataModel.type.asc(), MasterDataModel.value.asc()).all()
        finally:
            session.close()

    def get_by_id(self, item_id: int):
        session = self.db.get_session()
        try:
            return session.query(MasterDataModel).filter(MasterDataModel.id == item_id).first()
        finally:
            session.close()

    def create(self, item: MasterDataModel):
        session = self.db.get_session()
        try:
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def update(self, item_id: int, data: dict):
        session = self.db.get_session()
        try:
            item = session.query(MasterDataModel).filter(MasterDataModel.id == item_id).first()
            if not item:
                return None
            for key, val in data.items():
                if hasattr(item, key) and val is not None:
                    setattr(item, key, val)
            session.commit()
            session.refresh(item)
            return item
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
