
from collections import defaultdict

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
            # 1. Kiểm tra cuộc thi
            contest = session.query(ContestModel).filter(
                ContestModel.id == contest_id
            ).first()

            if not contest:
                return None

            # 2. Kiểm tra quyền xem thống kê
            if role == "organizer" and contest.created_by != user_id:
                return "FORBIDDEN"

            categories = session.query(CategoryModel).filter(
                CategoryModel.contest_id == contest_id
            ).all()

            category_map = {
                category.id: category.name
                for category in categories
            }

            # ==========================================
            # A. THỐNG KÊ ĐĂNG KÝ
            # ==========================================

            registration_rows = session.query(
                RegistrationModel.status,
                RegistrationModel.id
            ).filter(
                RegistrationModel.contest_id == contest_id
            ).all()

            registration_by_status = defaultdict(int)

            for status, registration_id in registration_rows:
                registration_by_status[status] += 1

            total_registrations = len(registration_rows)

            total_participants = session.query(
                RegistrationModel.participant_id
            ).filter(
                RegistrationModel.contest_id == contest_id
            ).distinct().count()

            registration_by_category = []

            for category in categories:
                count = session.query(RegistrationModel).filter(
                    RegistrationModel.contest_id == contest_id,
                    RegistrationModel.category_id == category.id
                ).count()

                registration_by_category.append({
                    "category_id": category.id,
                    "category_name": category.name,
                    "count": count
                })

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

            submission_by_category = []
            submission_by_status = defaultdict(int)

            for category in categories:
                count = sum(
                    1 for category_id, status in submission_rows
                    if category_id == category.id
                )

                submission_by_category.append({
                    "category_id": category.id,
                    "category_name": category.name,
                    "count": count
                })

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

            unique_flagged_submissions = len({
                row[0] for row in ai_rows
            })

            # ==========================================
            # D. PHÂN BỐ ĐIỂM ĐÁNH GIÁ
            # ==========================================

            score_rows = session.query(
                EvaluationModel.id.label("evaluation_id"),
                SubmissionModel.id.label("submission_id"),
                SubmissionModel.category_id.label("category_id"),
                EvaluationScoreModel.score.label("score"),
                CriterionModel.weight.label("weight"),
                CriterionModel.max_score.label("max_score")
            ).join(
                SubmissionModel,
                EvaluationModel.submission_id == SubmissionModel.id
            ).join(
                CategoryModel,
                SubmissionModel.category_id == CategoryModel.id
            ).join(
                EvaluationScoreModel,
                EvaluationScoreModel.evaluation_id == EvaluationModel.id
            ).join(
                CriterionModel,
                EvaluationScoreModel.criterion_id == CriterionModel.id
            ).filter(
                CategoryModel.contest_id == contest_id,
                EvaluationModel.confirmed.is_(True),
                CriterionModel.contest_id == contest_id
            ).all()

            # Gom điểm theo từng phiếu đánh giá
            evaluation_totals = {}

            for row in score_rows:
                evaluation_id = row.evaluation_id

                if evaluation_id not in evaluation_totals:
                    evaluation_totals[evaluation_id] = {
                        "weighted_score": 0.0,
                        "submission_id": row.submission_id,
                        "category_id": row.category_id,
                        "criterion_count": 0
                    }

                max_score = float(row.max_score or 0)
                weight = float(row.weight or 0)
                score = float(row.score or 0)

                if max_score > 0:
                    normalized_score = score / max_score
                    weighted_score = normalized_score * weight

                    evaluation_totals[evaluation_id][
                        "weighted_score"
                    ] += weighted_score

                    evaluation_totals[evaluation_id][
                        "criterion_count"
                    ] += 1

            score_bands = {
                "0-20": 0,
                "20-40": 0,
                "40-60": 0,
                "60-80": 0,
                "80-100": 0,
                "over-100": 0
            }

            evaluation_scores = []

            for evaluation_id, result in evaluation_totals.items():
                final_score = round(result["weighted_score"], 2)

                evaluation_scores.append({
                    "evaluation_id": evaluation_id,
                    "submission_id": result["submission_id"],
                    "category_id": result["category_id"],
                    "score": final_score
                })

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

            average_score = (
                round(
                    sum(item["score"] for item in evaluation_scores)
                    / len(evaluation_scores),
                    2
                )
                if evaluation_scores else 0
            )

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
                    "unique_submissions_checked": unique_flagged_submissions,
                    "by_type": dict(ai_by_type),
                    "by_decision": dict(ai_by_decision),
                    "by_type_and_decision": dict(ai_by_type_and_decision),
                    "note": (
                        "AI results are warnings for human review, "
                        "not final violation decisions."
                    )
                },
                "score_distribution": {
                    "confirmed_evaluations": len(evaluation_scores),
                    "average_score": average_score,
                    "score_bands": score_bands,
                    "evaluation_details": evaluation_scores,
                    "score_scale": "Weighted score based on criterion weight"
                }
            }

        finally:
            session.close()
