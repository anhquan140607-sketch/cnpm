from src.models import db

def update_ai_flag_decision(result_id, decision):
    """
    CNPM-71 / CNPM-59 (FE9): Cập nhật quyết định duyệt cờ AI (pending / flagged / cleared)
    """
    sql = """
        UPDATE ai_check_results
        SET decision = :decision
        WHERE id = :result_id
    """
    db.session.execute(db.text(sql), {"decision": decision, "result_id": result_id})
    db.session.commit()
    return {"result_id": result_id, "decision": decision}

def run_ai_verification(submission_id, phash_code=None, feature_vector=None):
    """
    CNPM-59 (FE9): Tích hợp AI Service phát hiện trùng lặp / AI-generated
    """
    # 1. Kiểm tra pHash trùng lặp
    # 2. Gọi API nhận diện ảnh AI
    # 3. Lưu kết quả vào bảng ai_check_results
    pass
