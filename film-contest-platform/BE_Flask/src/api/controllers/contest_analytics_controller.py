
from flask import Blueprint, g

from src.services.contest_analytics_service import ContestAnalyticsService
from src.api.middleware import authenticate_token, authorize_roles
from src.api.responses import success_response, error_response


analytics_bp = Blueprint(
    "contest_analytics",
    __name__,
    url_prefix="/api/v1/contests"
)

analytics_service = ContestAnalyticsService()


@analytics_bp.route("/<int:contest_id>/statistics", methods=["GET"])
@authenticate_token
@authorize_roles("organizer", "administrator")
def get_contest_statistics(contest_id):
    try:
        user_id = g.user.get("id")
        role = g.user.get("role")

        result = analytics_service.get_statistics(
            contest_id=contest_id,
            user_id=user_id,
            role=role
        )

        if result is None:
            return error_response(
                "Không tìm thấy cuộc thi",
                404,
                "CONTEST_NOT_FOUND"
            )

        if result == "FORBIDDEN":
            return error_response(
                "Bạn không có quyền xem thống kê cuộc thi này",
                403,
                "FORBIDDEN"
            )

        return success_response(
            result,
            "Lấy thống kê cuộc thi thành công"
        )

    except Exception as e:
        print(f"[FE15.1 Error] {str(e)}")

        return error_response(
            "Không thể tính toán thống kê cuộc thi",
            500,
            "ANALYTICS_ERROR"
        )
