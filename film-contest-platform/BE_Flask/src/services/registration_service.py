from src.infrastructure.repositories.registration_repository import RegistrationRepository
from src.infrastructure.models.registration_model import RegistrationModel
from src.domain.exceptions import NotFoundException, AppException

class RegistrationService:
    def __init__(self):
        self.repo = RegistrationRepository()

    def register_contest(self, participant_id: int, contest_id: int, category_id: int):
        reg = RegistrationModel(
            participant_id=participant_id,
            contest_id=contest_id,
            category_id=category_id,
            status='pending'
        )
        try:
            saved = self.repo.create(reg)
            return saved.to_dict()
        except Exception as e:
            raise AppException("Bạn đã đăng ký hạng mục này trong cuộc thi rồi hoặc thông tin không hợp lệ", 400)

    def get_contest_registrations(self, contest_id: int, status_filter: str = None):
        return self.repo.get_by_contest(contest_id, status_filter)

    def review_registration(self, reg_id: int, status: str, reason: str = None):
        if status not in ('approved', 'rejected', 'pending'):
            raise AppException("Trạng thái duyệt phải là 'approved' hoặc 'rejected'", 400)
        updated = self.repo.review(reg_id, status, reason)
        if not updated:
            raise NotFoundException("Không tìm thấy đơn đăng ký")
        return updated.to_dict()
