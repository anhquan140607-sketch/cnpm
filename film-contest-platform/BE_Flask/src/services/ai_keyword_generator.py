
import os
import base64
import mimetypes
import json

from PIL import Image, UnidentifiedImageError


class KeywordGenerationError(Exception):
    """Lỗi trong quá trình tạo từ khóa."""
    pass


class _ImageValidator:
    """Kiểm tra tính hợp lệ của ảnh đầu vào."""

    MAX_SIZE = 20 * 1024 * 1024

    ALLOWED_FORMATS = {
        "JPEG": ("image/jpeg", {".jpg", ".jpeg"}),
        "PNG": ("image/png", {".png"}),
        "WEBP": ("image/webp", {".webp"}),
        "GIF": ("image/gif", {".gif"})
    }

    @classmethod
    def validate(cls, image_path):
        if not isinstance(image_path, (str, os.PathLike)):
            raise KeywordGenerationError(
                "Đường dẫn ảnh không hợp lệ."
            )

        if not os.path.isfile(image_path):
            raise KeywordGenerationError(
                "Không tìm thấy file ảnh."
            )

        extension = os.path.splitext(image_path)[1].lower()

        if not any(
            extension in extensions
            for extensions in (
                item[1] for item in cls.ALLOWED_FORMATS.values()
            )
        ):
            raise KeywordGenerationError(
                "Định dạng ảnh không được hỗ trợ."
            )

        file_size = os.path.getsize(image_path)

        if file_size == 0:
            raise KeywordGenerationError(
                "File ảnh đang trống."
            )

        if file_size > cls.MAX_SIZE:
            raise KeywordGenerationError(
                "Ảnh vượt quá dung lượng 20MB."
            )

        try:
            with Image.open(image_path) as image:
                image_format = image.format

                if image_format not in cls.ALLOWED_FORMATS:
                    raise KeywordGenerationError(
                        "Định dạng ảnh không được hỗ trợ."
                    )

                expected_mime, allowed_extensions = (
                    cls.ALLOWED_FORMATS[image_format]
                )

                if extension not in allowed_extensions:
                    raise KeywordGenerationError(
                        "Phần mở rộng file không khớp với nội dung ảnh."
                    )

                image.verify()

            mime_type, _ = mimetypes.guess_type(image_path)

            if mime_type != expected_mime:
                raise KeywordGenerationError(
                    "Định dạng ảnh không hợp lệ."
                )

            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

        except (UnidentifiedImageError, OSError, SyntaxError):
            raise KeywordGenerationError(
                "File không phải ảnh hợp lệ hoặc ảnh bị hỏng."
            )

        return image_data, expected_mime


class DemoKeywordGenerator:
    """Sinh từ khóa mẫu để kiểm thử khi không có API."""

    def generate_keywords(
        self,
        image_path,
        language="vi",
        keyword_count=10
    ):
        _ImageValidator.validate(image_path)

        if language not in ("vi", "en"):
            raise KeywordGenerationError(
                "Ngôn ngữ chỉ hỗ trợ vi hoặc en."
            )

        if (
            isinstance(keyword_count, bool)
            or not isinstance(keyword_count, int)
            or not 1 <= keyword_count <= 20
        ):
            raise KeywordGenerationError(
                "Số lượng từ khóa phải từ 1 đến 20."
            )

        if language == "vi":
            keywords = [
                "nhiếp ảnh",
                "ảnh minh họa",
                "chủ thể",
                "bố cục",
                "ánh sáng",
                "màu sắc",
                "không gian",
                "chi tiết",
                "góc chụp",
                "nghệ thuật"
            ]

            description = (
                "Đây là mô tả mẫu trong chế độ DEMO. "
                "Chương trình chưa phân tích nội dung thực tế của ảnh."
            )

        else:
            keywords = [
                "photography",
                "photo",
                "subject",
                "composition",
                "lighting",
                "colors",
                "space",
                "details",
                "camera angle",
                "art"
            ]

            description = (
                "This is a DEMO description. "
                "The program has not actually analyzed the image."
            )

        return {
            "keywords": keywords[:keyword_count],
            "description": description,
            "model": "DEMO-OFFLINE"
        }


class AIKeywordGenerator:
    """Tạo từ khóa thực tế bằng OpenAI API."""

    def __init__(self):
        from dotenv import load_dotenv

        load_dotenv()

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.5")

        if not self.api_key:
            raise KeywordGenerationError(
                "Chưa cấu hình OPENAI_API_KEY."
            )

        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key)

        except ImportError:
            raise KeywordGenerationError(
                "Chưa cài thư viện openai."
            )

    def generate_keywords(
        self,
        image_path,
        language="vi",
        keyword_count=10
    ):
        if language not in ("vi", "en"):
            raise KeywordGenerationError(
                "Ngôn ngữ chỉ hỗ trợ vi hoặc en."
            )

        if (
            isinstance(keyword_count, bool)
            or not isinstance(keyword_count, int)
            or not 1 <= keyword_count <= 20
        ):
            raise KeywordGenerationError(
                "Số lượng từ khóa phải từ 1 đến 20."
            )

        image_data, mime_type = _ImageValidator.validate(
            image_path
        )

        image_base64 = base64.b64encode(
            image_data
        ).decode("utf-8")

        data_url = (
            f"data:{mime_type};base64,{image_base64}"
        )

        language_name = (
            "Vietnamese" if language == "vi" else "English"
        )

        prompt = f"""
        Analyze this photograph for a photography contest.

        Generate exactly {keyword_count} relevant keywords.

        Write the keywords and description in {language_name}.

        Return only valid JSON with this structure:
        {{
            "keywords": ["keyword 1", "keyword 2"],
            "description": "Short image description"
        }}
        """

        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt
                            },
                            {
                                "type": "input_image",
                                "image_url": data_url
                            }
                        ]
                    }
                ]
            )

            result = json.loads(response.output_text)

            if not isinstance(result, dict):
                raise ValueError("Kết quả AI không hợp lệ.")

            keywords = result.get("keywords")
            description = result.get("description")

            if not isinstance(keywords, list):
                raise ValueError("Danh sách từ khóa không hợp lệ.")

            if not isinstance(description, str) or not description.strip():
                raise ValueError("Mô tả ảnh không hợp lệ.")

            keywords = [
                item.strip()
                for item in keywords
                if isinstance(item, str) and item.strip()
            ]

            keywords = list(dict.fromkeys(keywords))

            if len(keywords) < keyword_count:
                raise ValueError(
                    "AI trả về không đủ số lượng từ khóa."
                )

            return {
                "keywords": keywords[:keyword_count],
                "description": description.strip(),
                "model": self.model
            }

        except Exception as error:
            # Ghi lỗi chi tiết vào log nội bộ.
            import logging
            logging.exception(
                "FE14.1: Không thể tạo từ khóa bằng OpenAI."
            )

            raise KeywordGenerationError(
                "Không thể tạo từ khóa bằng AI. "
                "Vui lòng thử lại sau."
            ) from error
