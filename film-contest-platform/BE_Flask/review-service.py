from src.models import db

def verify_submission_manually(submission_id, reviewer_id, status, reason=None):
    """
    CNPM-120 (FE8): Ban tổ chức duyệt thủ công bài dự thi (Accepted/Rejected)
    """
    sql_update = """
        UPDATE submissions 
        SET status = :status, updated_at = CURRENT_TIMESTAMP
        WHERE id = :submission_id
    """
    db.session.execute(db.text(sql_update), {"status": status, "submission_id": submission_id})
    
    sql_log = """
        INSERT INTO submission_reviews (submission_id, reviewer_id, status, reason)
        VALUES (:submission_id, :reviewer_id, :status, :reason)
    """
    db.session.execute(db.text(sql_log), {
        "submission_id": submission_id,
        "reviewer_id": reviewer_id,
        "status": status,
        "reason": reason
    })
    
    db.session.commit()
    return {"submission_id": submission_id, "status": status, "reviewer_id": reviewer_id}

def check_user_has_role(user_id, required_roles):
    """
    CNPM-115 (FE1/FE10): Kiểm tra phân quyền RBAC
    """
    sql = """
        SELECT r.name 
        FROM roles r
        JOIN user_roles ur ON r.id = ur.role_id
        WHERE ur.user_id = :user_id
    """
    results = db.session.execute(db.text(sql), {"user_id": user_id}).fetchall()
    user_roles = [row[0] for row in results]
    return any(role in user_roles for role in required_roles)
