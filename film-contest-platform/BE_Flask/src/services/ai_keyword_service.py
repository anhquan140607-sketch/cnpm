
import os

from src.services.ai_keyword_generator import (
    AIKeywordGenerator,
    DemoKeywordGenerator,
    KeywordGenerationError
)


class AIKeywordService:
    """
    Service quản lý chức năng FE14.1.
    """

    def __init__(self):
        # Mặc định sử dụng DEMO để không phát sinh chi phí API.
        self.mode = os.getenv("FE141_MODE", "demo").lower()

    def generate_keywords(
        self,
        image_path,
        language="vi",
        keyword_count=10
    ):
        """
        Tạo từ khóa cho hình ảnh.
        """

        # Chọn bộ tạo từ khóa theo chế độ.
        if self.mode == "demo":
            generator = DemoKeywordGenerator()

        elif self.mode == "openai":
            generator = AIKeywordGenerator()

        else:
            raise KeywordGenerationError(
                "FE141_MODE chỉ hỗ trợ demo hoặc openai."
            )

        # Thực hiện tạo từ khóa.
        result = generator.generate_keywords(
            image_path=image_path,
            language=language,
            keyword_count=keyword_count
        )

        # Bổ sung thông tin chế độ sử dụng.
        result["mode"] = self.mode

        return result
