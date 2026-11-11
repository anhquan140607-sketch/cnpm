from datetime import datetime
from src.infrastructure.repositories.contest_repository import ContestRepository
from src.infrastructure.models.contest_model import ContestModel
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.models.criterion_model import CriterionModel
from src.domain.exceptions import NotFoundException, AppException

class ContestService:
    def __init__(self):
        self.contest_repo = ContestRepository()

    def list_contests(self, status: str = None, page: int = 1, limit: int = 20):
        contests, total = self.contest_repo.list_contests(status, page, limit)
        return {
            'contests': [c.to_dict() for c in contests],
            'meta': {
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': (total + limit - 1) // limit if limit else 1
            }
        }

    def get_contest_details(self, contest_id: int):
        contest, categories, criteria = self.contest_repo.get_by_id(contest_id)
        if not contest:
            raise NotFoundException("Không tìm thấy cuộc thi")

        res = contest.to_dict()
        res['categories'] = [cat.to_dict() for cat in categories]
        res['criteria'] = [crit.to_dict() for crit in criteria]
        return res

    def create_contest(self, organizer_id: int, data: dict):
        contest = ContestModel(
            title=data.get('title'),
            theme=data.get('theme'),
            description=data.get('description'),
            regulations=data.get('regulations'),
            submission_start=datetime.fromisoformat(data['submission_start']) if isinstance(data['submission_start'], str) else data['submission_start'],
            submission_end=datetime.fromisoformat(data['submission_end']) if isinstance(data['submission_end'], str) else data['submission_end'],
            judging_start=datetime.fromisoformat(data['judging_start']) if isinstance(data['judging_start'], str) else data['judging_start'],
            judging_end=datetime.fromisoformat(data['judging_end']) if isinstance(data['judging_end'], str) else data['judging_end'],
            status='draft',
            config_locked=False,
            created_by=organizer_id
        )
        saved = self.contest_repo.create(contest)
        return saved.to_dict()

    def update_contest(self, user_id: int, contest_id: int, data: dict):
        contest, _, _ = self.contest_repo.get_by_id(contest_id)
        if not contest:
            raise NotFoundException("Không tìm thấy cuộc thi")
        if contest.config_locked and 'config_locked' not in data:
            raise AppException("Cuộc thi đã bị khóa cấu hình, không thể chỉnh sửa thể lệ", 400)

        updated = self.contest_repo.update(contest_id, data)
        return updated.to_dict()

    def add_category(self, user_id: int, contest_id: int, data: dict):
        cat = CategoryModel(
            contest_id=contest_id,
            name=data['name'],
            max_photos_per_participant=data.get('max_photos_per_participant', 5),
            submission_rules=data.get('submission_rules'),
            award_structure=data.get('award_structure')
        )
        saved = self.contest_repo.add_category(cat)
        return saved.to_dict()

    def add_criterion(self, user_id: int, contest_id: int, data: dict):
        crit = CriterionModel(
            contest_id=contest_id,
            category_id=data.get('category_id'),
            name=data['name'],
            description=data.get('description'),
            weight=data['weight'],
            max_score=data.get('max_score', 10.0)
        )
        saved = self.contest_repo.add_criterion(crit)
        return saved.to_dict()
