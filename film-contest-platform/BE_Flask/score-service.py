from src.models import db

def calculate_and_rank_submissions(contest_id, category_id=None):
    """
    Task CNPM-64 (FE11): Tính toán tổng điểm trung bình có trọng số cho các bài thi
    và trả về danh sách xếp hạng (Leaderboard Ranking) tự động.
    """
    query_sql = """
        WITH judge_scores AS (
            SELECT 
                e.submission_id,
                e.judge_id,
                SUM(es.score * (sc.weight_percentage / 100.0)) AS total_judge_score
            FROM evaluations e
            JOIN evaluation_scores es ON e.id = es.evaluation_id
            JOIN scoring_criteria sc ON es.criterion_id = sc.id
            WHERE e.confirmed = TRUE
            GROUP BY e.submission_id, e.judge_id, e.id
        ),
        final_submission_scores AS (
            SELECT 
                js.submission_id,
                ROUND(AVG(js.total_judge_score)::numeric, 2) AS final_score,
                COUNT(js.judge_id) AS total_judges_reviewed
            FROM judge_scores js
            GROUP BY js.submission_id
        )
        SELECT 
            s.id AS submission_id,
            s.title,
            s.participant_id,
            u.full_name AS participant_name,
            s.category_id,
            COALESCE(fss.final_score, 0.00) AS final_score,
            COALESCE(fss.total_judges_reviewed, 0) AS total_reviews,
            DENSE_RANK() OVER (
                PARTITION BY s.category_id 
                ORDER BY COALESCE(fss.final_score, 0) DESC
            ) AS rank_position
        FROM submissions s
        JOIN users u ON s.participant_id = u.id
        LEFT JOIN final_submission_scores fss ON s.id = fss.submission_id
        WHERE s.status = 'accepted'
    """
    
    result = db.session.execute(db.text(query_sql)).fetchall()
    
    ranking_list = []
    for row in result:
        ranking_list.append({
            "submission_id": row.submission_id,
            "title": row.title,
            "participant_name": row.participant_name,
            "category_id": row.category_id,
            "final_score": float(row.final_score),
            "total_reviews": row.total_reviews,
            "rank": row.rank_position
        })
        
    return ranking_list