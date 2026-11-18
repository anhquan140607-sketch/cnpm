
import os

from flask import Blueprint, request

from src.services.ai_keyword_service import (
    AIKeywordService,
    KeywordGenerationError
)
from src.api.responses import success_response, error_response


ai_keyword_bp = Blueprint(
    "ai_keyword",
    __name__,
    url_prefix="/api/v1/ai"
)

ai_keyword_service = AIKeywordService()

# Xác định thư mục backend
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

# Chỉ cho phép xử lý ảnh trong hai thư mục này
ALLOWED_IMAGE_DIRS = [
    os.path.join(BASE_DIR, "uploads"),
    os.path.join(BASE_DIR, "test_images")
]


def is_allowed_image_path(image_path):
    """Kiểm tra ảnh có nằm trong thư mục được phép không."""

    if not isinstance(image_path, str) or not image_path.strip():
        return False

    absolute_path = os.path.realpath(image_path)

    for directory in ALLOWED_IMAGE_DIRS:
        allowed_directory = os.path.realpath(directory)

        try:
            if os.path.commonpath(
                [absolute_path, allowed_directory]
            ) == allowed_directory:
                return True
        except ValueError:
            continue

    return False


@ai_keyword_bp.route("/generate-keywords", methods=["POST"])
def generate_keywords():
    """
    FE14.1 - Tự động tạo từ khóa cho ảnh.
    Nhận đường dẫn ảnh và trả về danh sách từ khóa.
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response(
            "Dữ liệu gửi lên phải là JSON object hợp lệ",
            400
        )

    image_path = data.get("image_path")
    language = data.get("language", "vi")
    keyword_count = data.get("keyword_count", 10)

    if not isinstance(image_path, str) or not image_path.strip():
        return error_response(
            "Vui lòng cung cấp image_path hợp lệ",
            400
        )

    if (
        isinstance(keyword_count, bool)
        or not isinstance(keyword_count, int)
        or not 1 <= keyword_count <= 20
    ):
        return error_response(
            "keyword_count phải là số nguyên từ 1 đến 20",
            400
        )

    if language not in ["vi", "en"]:
        return error_response(
            "language chỉ hỗ trợ vi hoặc en",
            400
        )

    try:
        image_path = os.path.realpath(image_path)

        if not is_allowed_image_path(image_path):
            return error_response(
                "Đường dẫn ảnh không nằm trong thư mục được phép",
                403
            )

        result = ai_keyword_service.generate_keywords(
            image_path=image_path,
            language=language,
            keyword_count=keyword_count
        )

        return success_response(
            result,
            "Tạo từ khóa cho ảnh thành công",
            200
        )

    except KeywordGenerationError as e:
        return error_response(str(e), 400)

    except Exception:
        return error_response(
            "Có lỗi xảy ra khi tạo từ khóa cho ảnh",
            500
        )
