
import re
import unicodedata


def normalize_text(value):
    """Chuẩn hóa tiếng Việt để so khớp từ khóa không phân biệt dấu."""
    if not value:
        return ""

    value = str(value).lower()
    value = unicodedata.normalize("NFD", value)
    value = "".join(
        char for char in value
        if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def tokenize(value):
    """Tách văn bản thành tập hợp từ."""
    return {
        word for word in normalize_text(value).split()
        if len(word) > 1
    }


class AICategoryService:
    """
    Gợi ý hạng mục bằng cách đối chiếu từ khóa.
    Đây là thuật toán hỗ trợ, không phải AI phân tích hình ảnh.
    """

    @staticmethod
    def suggest_category(submission, categories):
        if not categories:
            return {
                "suggestion": None,
                "alternatives": [],
                "message": "Cuộc thi chưa có hạng mục nào."
            }

        submission_text = " ".join([
            submission.title or "",
            submission.description or "",
            submission.keywords or ""
        ])

        submission_words = tokenize(submission_text)
        scored_categories = []

        for category in categories:
            category_name = category.name or ""
            category_rules = category.submission_rules or ""

            name_words = tokenize(category_name)
            rule_words = tokenize(category_rules)

            # Tên hạng mục có trọng số cao hơn quy định.
            name_matches = submission_words & name_words
            rule_matches = submission_words & rule_words

            score = (
                len(name_matches) * 3
                + len(rule_matches)
            )

            matched_words = sorted(name_matches | rule_matches)

            scored_categories.append({
                "category_id": category.id,
                "category_name": category.name,
                "score": score,
                "matched_keywords": matched_words,
                "reason": (
                    "Có từ khóa phù hợp: " + ", ".join(matched_words)
                    if matched_words
                    else "Chưa tìm thấy từ khóa trùng khớp rõ ràng."
                )
            })

        scored_categories.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        best = scored_categories[0]

        # Không khẳng định có gợi ý đáng tin nếu không có từ khóa khớp.
        if best["score"] == 0:
            suggestion = None
            message = (
                "Chưa đủ thông tin để đề xuất hạng mục. "
                "Organizer cần tự chọn hạng mục phù hợp."
            )
        else:
            suggestion = best
            message = "Đã tạo gợi ý hạng mục bằng đối chiếu từ khóa."

        return {
            "suggestion": suggestion,
            "alternatives": scored_categories,
            "method": "keyword_matching",
            "message": message
        }
