import { query } from '../../database/db.js';
import { logActivity } from '../../common/middleware/logger.middleware.js';

export class VerificationService {
  async listSubmissionsForVerification(contestId?: number, status?: string, page = 1, limit = 20) {
    const offset = (page - 1) * limit;
    let sql = `
      SELECT s.*, 
             u.name as participant_name, u.email as participant_email,
             cat.name as category_name, c.title as contest_title,
             f.frame_number, f.shooting_location,
             fr.roll_name, b.value as film_brand, stk.value as film_stock,
             (SELECT COUNT(*) FROM ai_check_results ac WHERE ac.submission_id = s.id AND ac.decision = 'flagged') as flag_count
      FROM submissions s
      JOIN users u ON s.participant_id = u.id
      JOIN categories cat ON s.category_id = cat.id
      JOIN contests c ON cat.contest_id = c.id
      JOIN frames f ON s.frame_id = f.id
      JOIN film_rolls fr ON f.film_roll_id = fr.id
      LEFT JOIN master_data b ON fr.film_brand_id = b.id
      LEFT JOIN master_data stk ON fr.film_stock_id = stk.id
      WHERE 1=1
    `;
    let countSql = `
      SELECT COUNT(*) FROM submissions s 
      JOIN categories cat ON s.category_id = cat.id 
      WHERE 1=1
    `;
    const params: any[] = [];

    if (contestId) {
      params.push(contestId);
      sql += ` AND cat.contest_id = $${params.length}`;
      countSql += ` AND cat.contest_id = $${params.length}`;
    }

    if (status) {
      params.push(status);
      sql += ` AND s.status = $${params.length}`;
      countSql += ` AND s.status = $${params.length}`;
    }

    sql += ` ORDER BY s.submitted_at ASC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(limit, offset);

    const [dataRes, countRes] = await Promise.all([
      query(sql, params),
      query(countSql, params.slice(0, params.length - 2)),
    ]);

    const total = parseInt(countRes.rows[0].count, 10);
    return {
      submissions: dataRes.rows,
      meta: { page, limit, total, totalPages: Math.ceil(total / limit) },
    };
  }

  async verifySubmission(
    organizerId: number,
    submissionId: number,
    decision: 'accepted' | 'rejected' | 'needs_revision',
    reason?: string
  ) {
    const subRes = await query(`SELECT id, status FROM submissions WHERE id = $1`, [submissionId]);
    if (subRes.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy bài dự thi' };

    const result = await query(
      `UPDATE submissions 
       SET status = $1, rejection_reason = $2, updated_at = CURRENT_TIMESTAMP
       WHERE id = $3
       RETURNING *`,
      [decision, reason || null, submissionId]
    );

    await logActivity(organizerId, 'VERIFY_SUBMISSION', 'SUBMISSION', submissionId, {
      decision,
      reason,
    });

    return result.rows[0];
  }

  async recordAiCheckResult(data: {
    submission_id: number;
    type: 'duplicate' | 'ai_generated' | 'content_moderation';
    score: number;
    matched_submission_id?: number | null;
    details?: any;
    decision: 'pending' | 'flagged' | 'cleared';
  }) {
    const result = await query(
      `INSERT INTO ai_check_results (submission_id, type, score, matched_submission_id, details, decision)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [
        data.submission_id,
        data.type,
        data.score,
        data.matched_submission_id || null,
        data.details ? JSON.stringify(data.details) : null,
        data.decision,
      ]
    );
    return result.rows[0];
  }

  async getAiResultsForSubmission(submissionId: number) {
    const result = await query(
      `SELECT * FROM ai_check_results WHERE submission_id = $1 ORDER BY checked_at DESC`,
      [submissionId]
    );
    return result.rows;
  }
}

export const verificationService = new VerificationService();
