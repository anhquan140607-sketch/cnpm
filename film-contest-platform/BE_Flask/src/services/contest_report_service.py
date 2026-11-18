
import csv
import io

from src.services.contest_analytics_service import ContestAnalyticsService


class ContestReportService:

    def __init__(self):
        self.analytics_service = ContestAnalyticsService()

    def export_csv(self, contest_id: int, user_id: int, role: str):
        """
        Xuất báo cáo thống kê cuộc thi dưới dạng CSV.

        Trả về:
        - None: Không tìm thấy cuộc thi.
        - "FORBIDDEN": Người dùng không có quyền truy cập.
        - Chuỗi CSV: Xuất báo cáo thành công.
        """

        # 1. Lấy dữ liệu từ chức năng FE15.1
        statistics = self.analytics_service.get_statistics(
            contest_id=contest_id,
            user_id=user_id,
            role=role
        )

        if statistics is None:
            return None

        if statistics == "FORBIDDEN":
            return "FORBIDDEN"

        # 2. Tạo vùng nhớ để ghi nội dung CSV
        output = io.StringIO(newline="")

        writer = csv.writer(output)

        # 3. Tiêu đề báo cáo
        writer.writerow(["BAO CAO THONG KE CUOC THI"])
        writer.writerow([])

        contest = statistics["contest"]

        writer.writerow(["THONG TIN CUOC THI"])
        writer.writerow(["Ma cuoc thi", contest["id"]])
        writer.writerow(["Ten cuoc thi", contest["title"]])
        writer.writerow(["Trang thai", contest["status"]])
        writer.writerow([])

        # 4. Thống kê đăng ký
        registrations = statistics["registrations"]

        writer.writerow(["THONG KE DANG KY"])
        writer.writerow(["Tong so dang ky", registrations["total"]])
        writer.writerow([
            "So thi sinh duy nhat",
            registrations["unique_participants"]
        ])

        writer.writerow(["Trang thai dang ky", "So luong"])

        for status, count in sorted(
            registrations["by_status"].items()
        ):
            writer.writerow([status, count])

        writer.writerow([])
        writer.writerow(["Dang ky theo danh muc"])
        writer.writerow(["Ma danh muc", "Ten danh muc", "So luong"])

        for category in registrations["by_category"]:
            writer.writerow([
                category["category_id"],
                category["category_name"],
                category["count"]
            ])

        writer.writerow([])

        # 5. Thống kê bài dự thi
        submissions = statistics["submissions"]

        writer.writerow(["THONG KE BAI DU THI"])
        writer.writerow(["Tong so bai du thi", submissions["total"]])

        writer.writerow(["Trang thai bai du thi", "So luong"])

        for status, count in sorted(
            submissions["by_status"].items()
        ):
            writer.writerow([status, count])

        writer.writerow([])
        writer.writerow(["Bai du thi theo danh muc"])
        writer.writerow(["Ma danh muc", "Ten danh muc", "So luong"])

        for category in submissions["by_category"]:
            writer.writerow([
                category["category_id"],
                category["category_name"],
                category["count"]
            ])

        writer.writerow([])

        # 6. Thống kê kết quả kiểm tra AI
        ai_flags = statistics["ai_flags"]

        writer.writerow(["THONG KE KIEM TRA AI"])
        writer.writerow([
            "Tong so luot kiem tra",
            ai_flags["total_check_records"]
        ])
        writer.writerow([
            "Tong so ket qua bi danh dau",
            ai_flags["total_flagged_records"]
        ])
        writer.writerow([
            "So bai du thi da duoc kiem tra",
            ai_flags["unique_submissions_checked"]
        ])
        writer.writerow([
            "So bai du thi co ket qua bi danh dau",
            ai_flags["unique_flagged_submissions"]
        ])

        writer.writerow([])
        writer.writerow(["Thong ke theo loai kiem tra", "So luong"])

        for check_type, count in sorted(
            ai_flags["by_type"].items()
        ):
            writer.writerow([check_type, count])

        writer.writerow([])
        writer.writerow(["Thong ke theo quyet dinh", "So luong"])

        for decision, count in sorted(
            ai_flags["by_decision"].items()
        ):
            writer.writerow([decision, count])

        writer.writerow([])
        writer.writerow([
            "Loai kiem tra - Quyet dinh",
            "So luong"
        ])

        for key, count in sorted(
            ai_flags["by_type_and_decision"].items()
        ):
            writer.writerow([key, count])

        writer.writerow([])
        writer.writerow(["Ghi chu", ai_flags["note"]])
        writer.writerow([])

        # 7. Thống kê điểm đánh giá
        scores = statistics["score_distribution"]

        writer.writerow(["THONG KE DIEM DANH GIA"])
        writer.writerow([
            "So phieu danh gia hop le",
            scores["confirmed_evaluations"]
        ])
        writer.writerow([
            "Diem trung binh",
            scores["average_score"]
        ])
        writer.writerow(["Thang diem", scores["score_scale"]])

        writer.writerow([])
        writer.writerow(["Phan bo diem", "So bai du thi"])

        for score_range, count in scores["score_bands"].items():
            writer.writerow([score_range, count])

        # 8. Chi tiết điểm từng bài dự thi
        writer.writerow([])
        writer.writerow(["CHI TIET DIEM TUNG BAI DU THI"])
        writer.writerow([
            "Ma bai du thi",
            "Ma danh muc",
            "Diem cuoi cung",
            "So giam khao"
        ])

        for item in scores["evaluation_details"]:
            writer.writerow([
                item["submission_id"],
                item["category_id"],
                item["score"],
                item["total_judges"]
            ])

        # 9. Trả nội dung CSV
        return output.getvalue()
