
from collections import defaultdict

from sqlalchemy import func

from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.contest_model import ContestModel
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.models.registration_model import RegistrationModel
from src.infrastructure.models.submission_model import SubmissionModel
from src.infrastructure.models.ai_check_result_model import AICheckResultModel
from src.infrastructure.models.evaluation_model import EvaluationModel
from src.infrastructure.models.evaluation_score_model import EvaluationScoreModel
from src.infrastructure.models.criterion_model import CriterionModel


class ContestAnalyticsService:

    def __init__(self):
        self.db = FactoryDatabase.get_database()

    def get_statistics(self, contest_id: int, user_id: int, role: str):
        session = self.db.get_session()

        try:
            # ==========================================
            # 1. KIỂM TRA CUỘC THI VÀ QUYỀN TRUY CẬP
            # ==========================================

            contest = session.query(ContestModel).filter(
                ContestModel.id == contest_id
            ).first()

            if not contest:
                return None

            # Organizer chỉ được xem thống kê cuộc thi của mình
            if role == "organizer" and contest.created_by != user_id:
                return "FORBIDDEN"

            # ==========================================
            # 2. LẤY DANH SÁCH DANH MỤC
            # ==========================================

            categories = session.query(CategoryModel).filter(
                CategoryModel.contest_id == contest_id
            ).all()

            # ==========================================
            # A. THỐNG KÊ ĐĂNG KÝ
            # ==========================================

            registration_rows = session.query(
                RegistrationModel.status
            ).filter(
                RegistrationModel.contest_id == contest_id
            ).all()

            registration_by_status = defaultdict(int)

            for (status,) in registration_rows:
                registration_by_status[status] += 1

            total_registrations = len(registration_rows)

            total_participants = session.query(
                func.count(func.distinct(
                    RegistrationModel.participant_id
                ))
            ).filter(
                RegistrationModel.contest_id == contest_id
            ).scalar() or 0

            # Đếm đăng ký theo danh mục bằng GROUP BY
            registration_category_rows = session.query(
                RegistrationModel.category_id,
                func.count(RegistrationModel.id)
            ).filter(
                RegistrationModel.contest_id == contest_id
            ).group_by(
                RegistrationModel.category_id
            ).all()

            registration_count_map = {
                category_id: count
                for category_id, count in registration_category_rows
            }

            registration_by_category = [
                {
                    "category_id": category.id,
                    "category_name": category.name,
                    "count": registration_count_map.get(category.id, 0)
                }
                for category in categories
            ]

            # ==========================================
            # B. THỐNG KÊ BÀI DỰ THI
            # ==========================================

            submission_rows = session.query(
                SubmissionModel.category_id,
                SubmissionModel.status
            ).join(
                CategoryModel,
                SubmissionModel.category_id == CategoryModel.id
            ).filter(
                CategoryModel.contest_id == contest_id
            ).all()

            total_submissions = len(submission_rows)

            submission_by_status = defaultdict(int)

            submission_category_rows = session.query(
                SubmissionModel.category_id,
                func.count(SubmissionModel.id)
            ).join(
                CategoryModel,
                SubmissionModel.category_id == CategoryModel.id
            ).filter(
                CategoryModel.contest_id == contest_id
            ).group_by(
                SubmissionModel.category_id
            ).all()

            submission_count_map = {
                category_id: count
                for category_id, count in submission_category_rows
            }

            submission_by_category = [
                {
                    "category_id": category.id,
                    "category_name": category.name,
                    "count": submission_count_map.get(category.id, 0)
                }
                for category in categories
            ]

            for category_id, status in submission_rows:
                submission_by_status[status] += 1

            # ==========================================
            # C. THỐNG KÊ CÁC KẾT QUẢ KIỂM TRA AI
            # ==========================================

            ai_rows = session.query(
                AICheckResultModel.submission_id,
                AICheckResultModel.type,
                AICheckResultModel.decision
            ).join(
                SubmissionModel,
                AICheckResultModel.submission_id == SubmissionModel.id
            ).join(
                CategoryModel,
                SubmissionModel.category_id == CategoryModel.id
            ).filter(
                CategoryModel.contest_id == contest_id
            ).all()

            ai_by_type = defaultdict(int)
            ai_by_decision = defaultdict(int)
            ai_by_type_and_decision = defaultdict(int)

            for submission_id, check_type, decision in ai_rows:
                ai_by_type[check_type] += 1
                ai_by_decision[decision] += 1

                ai_by_type_and_decision[
                    f"{check_type} - {decision}"
                ] += 1

            # Chỉ đếm các lượt kiểm tra có decision = flagged
            flagged_rows = [
                row for row in ai_rows
                if row[2] == "flagged"
            ]

            # Số bài dự thi có ít nhất một kết quả bị đánh dấu
            unique_flagged_submissions = len({
                row[0] for row in flagged_rows
            })

            # Số bài dự thi đã được kiểm tra AI
            unique_checked_submissions = len({
                row[0] for row in ai_rows
            })

            # ==========================================
            # D. PHÂN BỐ ĐIỂM ĐÁNH GIÁ
            # ==========================================

            # D1. Lấy các phiếu đánh giá đã xác nhận
            confirmed_evaluations = session.query(
                EvaluationModel.id,
                EvaluationModel.submission_id,
                SubmissionModel.category_id
            ).join(
                SubmissionModel,
                EvaluationModel.submission_id == SubmissionModel.id
            ).join(
                CategoryModel,
                SubmissionModel.category_id == CategoryModel.id
            ).filter(
                CategoryModel.contest_id == contest_id,
                EvaluationModel.confirmed.is_(True)
            ).all()

            # D2. Lấy các tiêu chí thuộc cuộc thi
            all_criteria = session.query(
                CriterionModel.id,
                CriterionModel.category_id,
                CriterionModel.weight,
                CriterionModel.max_score
            ).filter(
                CriterionModel.contest_id == contest_id
            ).all()

            # D3. Nhóm tiêu chí chung và tiêu chí riêng
            global_criteria = []
            category_criteria = defaultdict(list)

            for criterion in all_criteria:
                if criterion.category_id is None:
                    global_criteria.append(criterion)
                else:
                    category_criteria[criterion.category_id].append(
                        criterion
                    )

            # D4. Lấy điểm của các phiếu đánh giá
            evaluation_ids = [
                evaluation.id
                for evaluation in confirmed_evaluations
            ]

            scores_by_evaluation = defaultdict(dict)

            if evaluation_ids:
                score_rows = session.query(
                    EvaluationScoreModel.evaluation_id,
                    EvaluationScoreModel.criterion_id,
                    EvaluationScoreModel.score
                ).filter(
                    EvaluationScoreModel.evaluation_id.in_(evaluation_ids)
                ).all()

                for row in score_rows:
                    scores_by_evaluation[row.evaluation_id][
                        row.criterion_id
                    ] = float(row.score)

            # D5. Tính điểm hợp lệ cho từng phiếu
            valid_evaluations = []

            for evaluation in confirmed_evaluations:

                submission_id = evaluation.submission_id
                category_id = evaluation.category_id

                # Kết hợp tiêu chí chung và tiêu chí riêng
                applicable_criteria = (
                    global_criteria
                    + category_criteria.get(category_id, [])
                )

                # Không có tiêu chí thì không thể tính điểm
                if not applicable_criteria:
                    continue

                # Kiểm tra ID tiêu chí không bị trùng
                expected_criterion_ids = {
                    criterion.id
                    for criterion in applicable_criteria
                }

                if len(expected_criterion_ids) != len(applicable_criteria):
                    continue

                # Tổng trọng số phải bằng 100%
                total_weight = sum(
                    float(criterion.weight)
                    for criterion in applicable_criteria
                )

                if abs(total_weight - 100.0) > 0.01:
                    continue

                evaluation_scores_data = scores_by_evaluation.get(
                    evaluation.id, {}
                )

                actual_criterion_ids = set(
                    evaluation_scores_data.keys()
                )

                # Phiếu phải có chính xác các tiêu chí được áp dụng
                if expected_criterion_ids != actual_criterion_ids:
                    continue

                weighted_total = 0.0
                valid_score = True

                # Tính điểm có trọng số
                for criterion in applicable_criteria:

                    score = evaluation_scores_data[criterion.id]
                    max_score = float(criterion.max_score)
                    weight = float(criterion.weight)

                    # Kiểm tra điểm tối đa và trọng số
                    if max_score <= 0 or weight <= 0:
                        valid_score = False
                        break

                    # Điểm phải nằm trong khoảng hợp lệ
                    if score < 0 or score > max_score:
                        valid_score = False
                        break

                    normalized_score = score / max_score

                    weighted_total += normalized_score * weight

                if not valid_score:
                    continue

                valid_evaluations.append({
                    "evaluation_id": evaluation.id,
                    "submission_id": submission_id,
                    "category_id": category_id,
                    "score": round(weighted_total, 2)
                })

            # D6. Tổng hợp điểm theo từng bài dự thi
            submission_score_groups = defaultdict(list)

            for evaluation in valid_evaluations:
                submission_score_groups[
                    evaluation["submission_id"]
                ].append(evaluation["score"])

            evaluation_details = []

            for submission_id, scores in submission_score_groups.items():

                final_score = round(
                    sum(scores) / len(scores),
                    2
                )

                # Lấy category_id của bài dự thi
                category_id = next(
                    item["category_id"]
                    for item in valid_evaluations
                    if item["submission_id"] == submission_id
                )

                evaluation_details.append({
                    "submission_id": submission_id,
                    "category_id": category_id,
                    "score": final_score,
                    "total_judges": len(scores)
                })

            # D7. Sắp xếp kết quả theo submission_id
            evaluation_details.sort(
                key=lambda item: item["submission_id"]
            )

            # D8. Tính điểm trung bình của cuộc thi
            final_submission_scores = [
                item["score"]
                for item in evaluation_details
            ]

            average_score = (
                round(
                    sum(final_submission_scores)
                    / len(final_submission_scores),
                    2
                )
                if final_submission_scores else 0
            )

            # D9. Phân nhóm điểm theo từng bài dự thi
            score_bands = {
                "0-20": 0,
                "20-40": 0,
                "40-60": 0,
                "60-80": 0,
                "80-100": 0,
                "over-100": 0
            }

            for final_score in final_submission_scores:

                if final_score < 20:
                    score_bands["0-20"] += 1

                elif final_score < 40:
                    score_bands["20-40"] += 1

                elif final_score < 60:
                    score_bands["40-60"] += 1

                elif final_score < 80:
                    score_bands["60-80"] += 1

                elif final_score <= 100:
                    score_bands["80-100"] += 1

                else:
                    score_bands["over-100"] += 1

            # ==========================================
            # E. TRẢ KẾT QUẢ
            # ==========================================

            return {
                "contest": {
                    "id": contest.id,
                    "title": contest.title,
                    "status": contest.status
                },
                "registrations": {
                    "total": total_registrations,
                    "unique_participants": total_participants,
                    "by_status": dict(registration_by_status),
                    "by_category": registration_by_category
                },
                "submissions": {
                    "total": total_submissions,
                    "by_status": dict(submission_by_status),
                    "by_category": submission_by_category
                },
                "ai_flags": {
                    "total_check_records": len(ai_rows),
                    "total_flagged_records": len(flagged_rows),
                    "unique_submissions_checked": unique_checked_submissions,
                    "unique_flagged_submissions": unique_flagged_submissions,
                    "by_type": dict(ai_by_type),
                    "by_decision": dict(ai_by_decision),
                    "by_type_and_decision": dict(ai_by_type_and_decision),
                    "note": (
                        "AI results are warnings for human review, "
                        "not final violation decisions."
                    )
                },
                "score_distribution": {
                    # Giữ tên cũ để không ảnh hưởng frontend
                    "confirmed_evaluations": len(valid_evaluations),
                    "average_score": average_score,
                    "score_bands": score_bands,
                    "evaluation_details": evaluation_details,
                    "score_scale": "Weighted score based on criterion weight"
                }
            }

        finally:
            session.close()
