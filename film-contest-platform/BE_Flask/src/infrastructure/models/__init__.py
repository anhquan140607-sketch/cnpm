# Đăng ký toàn bộ 18 SQLAlchemy ORM Models khớp 1:1 với ERD.MD
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.contest_model import ContestModel
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.models.criterion_model import CriterionModel
from src.infrastructure.models.round_model import RoundModel
from src.infrastructure.models.registration_model import RegistrationModel
from src.infrastructure.models.master_data_model import MasterDataModel
from src.infrastructure.models.film_roll_model import FilmRollModel
from src.infrastructure.models.frame_model import FrameModel
from src.infrastructure.models.submission_model import SubmissionModel
from src.infrastructure.models.ai_check_result_model import AICheckResultModel
from src.infrastructure.models.judge_assignment_model import JudgeAssignmentModel
from src.infrastructure.models.evaluation_model import EvaluationModel
from src.infrastructure.models.evaluation_score_model import EvaluationScoreModel
from src.infrastructure.models.award_model import AwardModel
from src.infrastructure.models.archive_item_model import ArchiveItemModel
from src.infrastructure.models.activity_log_model import ActivityLogModel
from src.infrastructure.models.refresh_token_model import RefreshTokenModel

__all__ = [
    'UserModel',
    'ContestModel',
    'CategoryModel',
    'CriterionModel',
    'RoundModel',
    'RegistrationModel',
    'MasterDataModel',
    'FilmRollModel',
    'FrameModel',
    'SubmissionModel',
    'AICheckResultModel',
    'JudgeAssignmentModel',
    'EvaluationModel',
    'EvaluationScoreModel',
    'AwardModel',
    'ArchiveItemModel',
    'ActivityLogModel',
    'RefreshTokenModel'
]
