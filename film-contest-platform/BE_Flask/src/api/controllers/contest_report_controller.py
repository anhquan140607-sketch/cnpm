
from flask import Blueprint, g, Response, request
from datetime import datetime

from src.services.contest_report_service import ContestReportService
from src.api.middleware import authenticate_token, authorize_roles
from src.api.responses import error_response


report_bp = Blueprint(
    "contest_report",
    __name__,
    url_prefix="/api/v1/contests"
)

report_service = ContestReportService()


@report_bp.route("/<int:contest_id>/report/export", methods=["GET"])
@authenticate_token
@authorize_roles("organizer")
def export_contest_report(contest_id):
    try:
        # Chỉ hỗ trợ CSV ở phiên bản hiện tại
        file_format = request.args.get("format", "csv").lower()

        if file_format != "csv":
            return error_response(
                "Định dạng báo cáo không được hỗ trợ. Hiện chỉ hỗ trợ CSV.",
                400,
                "INVALID_FORMAT"
            )

        user_id = g.user.get("id")
        role = g.user.get("role")

        csv_content = report_service.export_csv(
            contest_id=contest_id,
            user_id=user_id,
            role=role
        )

        if csv_content is None:
            return error_response(
                "Không tìm thấy cuộc thi",
                404,
                "CONTEST_NOT_FOUND"
            )

        if csv_content == "FORBIDDEN":
            return error_response(
                "Bạn không có quyền xuất báo cáo cuộc thi này",
                403,
                "FORBIDDEN"
            )

        # UTF-8 BOM giúp Excel hiển thị tiếng Việt đúng
        csv_bytes = ("\ufeff" + csv_content).encode("utf-8")

        filename = (
            f"contest_{contest_id}_report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        return Response(
            csv_bytes,
            status=200,
            mimetype="text/csv",
            headers={
                "Content-Disposition": (
                    f'attachment; filename="{filename}"'
                )
            }
        )

    except Exception as e:
        print(f"[FE15.3 Error] {str(e)}")

        return error_response(
            "Không thể xuất báo cáo cuộc thi",
            500,
            "REPORT_EXPORT_ERROR"
        )
