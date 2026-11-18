
from flask import Blueprint, request, g

from src.api.middleware import authenticate_token, authorize_roles
from src.api.responses import success_response, error_response

from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.submission_model import SubmissionModel
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.models.contest_model import ContestModel

from src.services.ai_category_service import AICategoryService


ai_category_bp = Blueprint(
    "ai_category",
    __name__,
    url_prefix="/api/v1/ai"
)

category_service = AICategoryService()


def get_submission_and_categories(session, submission_id):
    submission = (
        session.query(SubmissionModel)
        .filter(SubmissionModel.id == submission_id)
        .first()
    )

    if not submission:
        return None, None, None

    # Xác định cuộc thi thông qua hạng mục hiện tại.
    current_category = (
        session.query(CategoryModel)
        .filter(CategoryModel.id == submission.category_id)
        .first()
    )

    if not current_category:
        return submission, None, None

    contest = (
        session.query(ContestModel)
        .filter(ContestModel.id == current_category.contest_id)
        .first()
    )

    if not contest:
        return submission, None, None

    categories = (
        session.query(CategoryModel)
        .filter(CategoryModel.contest_id == contest.id)
        .all()
    )

    return submission, contest, categories


def organizer_can_manage(contest):
    user = g.user

    # Administrator được quản lý mọi cuộc thi.
    if user.get("role") == "administrator":
        return True

    return (
        user.get("role") == "organizer"
        and contest.created_by == user.get("id")
    )


@ai_category_bp.route(
    "/submissions/<int:submission_id>/suggest-category",
    methods=["POST"]
)
@authenticate_token
@authorize_roles("organizer", "administrator")
def suggest_category(submission_id):
    session = FactoryDatabase.get_database().get_session()

    try:
        submission, contest, categories = (
            get_submission_and_categories(session, submission_id)
        )

        if not submission:
            return error_response("Không tìm thấy bài dự thi.", 404)

        if not contest:
            return error_response(
                "Không tìm thấy cuộc thi của bài dự thi.",
                404
            )

        if not organizer_can_manage(contest):
            return error_response(
                "Bạn không có quyền quản lý cuộc thi này.",
                403
            )

        result = category_service.suggest_category(
            submission,
            categories
        )

        return success_response(
            result,
            "Đã xử lý gợi ý hạng mục."
        )

    except Exception:
        session.rollback()
        return error_response(
            "Không thể tạo gợi ý hạng mục. Vui lòng thử lại.",
            500
        )

    finally:
        session.close()


@ai_category_bp.route(
    "/submissions/<int:submission_id>/metadata",
    methods=["PUT"]
)
@authenticate_token
@authorize_roles("organizer", "administrator")
def update_submission_metadata(submission_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("Dữ liệu gửi lên không hợp lệ.", 400)

    category_id = data.get("category_id")
    keywords = data.get("keywords")

    if not isinstance(category_id, int) or isinstance(category_id, bool):
        return error_response("category_id phải là số nguyên.", 400)

    if not isinstance(keywords, list):
        return error_response("keywords phải là một danh sách.", 400)

    if len(keywords) > 20:
        return error_response("Tối đa 20 từ khóa.", 400)

    cleaned_keywords = []

    for keyword in keywords:
        if not isinstance(keyword, str):
            return error_response("Mỗi từ khóa phải là chuỗi.", 400)

        keyword = keyword.strip()

        if keyword and keyword not in cleaned_keywords:
            cleaned_keywords.append(keyword)

    if any(len(keyword) > 50 for keyword in cleaned_keywords):
        return error_response(
            "Mỗi từ khóa không được vượt quá 50 ký tự.",
            400
        )

    keywords_text = ", ".join(cleaned_keywords)

    if len(keywords_text) > 500:
        return error_response(
            "Tổng nội dung từ khóa vượt quá 500 ký tự.",
            400
        )

    session = FactoryDatabase.get_database().get_session()

    try:
        submission, contest, categories = (
            get_submission_and_categories(session, submission_id)
        )

        if not submission:
            return error_response("Không tìm thấy bài dự thi.", 404)

        if not contest:
            return error_response(
                "Không tìm thấy cuộc thi của bài dự thi.",
                404
            )

        if not organizer_can_manage(contest):
            return error_response(
                "Bạn không có quyền quản lý cuộc thi này.",
                403
            )

        selected_category = next(
            (
                category for category in categories
                if category.id == category_id
            ),
            None
        )

        if not selected_category:
            return error_response(
                "Hạng mục không thuộc cuộc thi của bài dự thi.",
                400
            )

        submission.category_id = category_id
        submission.keywords = keywords_text

        session.commit()
        session.refresh(submission)

        return success_response(
            {
                "submission_id": submission.id,
                "category_id": submission.category_id,
                "category_name": selected_category.name,
                "keywords": cleaned_keywords
            },
            "Đã lưu hạng mục và từ khóa thành công."
        )

    except Exception:
        session.rollback()
        return error_response(
            "Không thể lưu thông tin bài dự thi.",
            500
        )

    finally:
        session.close()
