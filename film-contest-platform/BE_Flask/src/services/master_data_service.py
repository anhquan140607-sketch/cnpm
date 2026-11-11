from src.infrastructure.repositories.master_data_repository import MasterDataRepository
from src.infrastructure.models.master_data_model import MasterDataModel
from src.domain.exceptions import NotFoundException

class MasterDataService:
    def __init__(self):
        self.repo = MasterDataRepository()

    def get_all(self, type_filter: str = None, active_only: bool = True):
        items = self.repo.get_all(type_filter, active_only)
        return [item.to_dict() for item in items]

    def create(self, data: dict):
        item = MasterDataModel(
            type=data['type'],
            value=data['value'],
            description=data.get('description'),
            status=data.get('status', 'active')
        )
        saved = self.repo.create(item)
        return saved.to_dict()
