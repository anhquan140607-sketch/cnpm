import { query } from '../../database/db.js';
import { logActivity } from '../../common/middleware/logger.middleware.js';

export class JudgingService {
  // Organizer assigns judge
  async assignJudge(organizerId: number, judgeId: number, categoryId: number, roundId: number) {
    // Verify judge has role 'judge'
    const judgeRes = await query(`SELECT role FROM users WHERE id = $1`, [judgeId]);
    if (judgeRes.rowCount === 0 || judgeRes.rows[0].role !== 'judge') {
      throw { statusCode: 400, message: 'Người dùng được chọn không phải là giám khảo' };
    }

    try {
      const result = await query(
        `INSERT INTO judge_assignments (judge_id, category_id, round_id)
         VALUES ($1, $2, $3)
         RETURNING *`,
        [judgeId, categoryId, roundId]
      );
      await logActivity(organizerId, 'ASSIGN_JUDGE', 'JUDGE_ASSIGNMENT', result.rows[0].id, {
        judgeId,
        categoryId,
        roundId,
      });
      return result.rows[0];
    } catch (err: any) {
      if (err.code === '23505') {
        throw { statusCode: 409, message: 'Giám khảo đã được phân công vào hạng mục và vòng chấm này' };
      }
      throw err;
    }
  }

  // Judge views submissions in assigned categories
  async getJudgeWorkspace(judgeId: number) {
    const assignments = await query(
      `SELECT ja.*, cat.name as category_name, c.title as contest_title, r.name as round_name
       FROM judge_assignments ja
       JOIN categories cat ON ja.category_id = cat.id
       JOIN contests c ON cat.contest_id = c.id
       JOIN rounds r ON ja.round_id = r.id
       WHERE ja.judge_id = $1`,
      [judgeId]
    );

    // Get submissions for each assigned category (only accepted ones, FR-8.3)
    const categoryIds = assignments.rows.map((a) => a.category_id);
    if (categoryIds.length === 0) {
      return { assignments: [], submissions: [] };
    }

    const submissionsRes = await query(
      `SELECT s.id, s.category_id, s.title, s.description, s.image_path, s.thumbnail_path,
              s.keywords, s.submitted_at,
              cat.name as category_name,
              e.id as evaluation_id, e.confirmed as evaluation_confirmed, e.comment as evaluation_comment
       FROM submissions s
       JOIN categories cat ON s.category_id = cat.id
       LEFT JOIN evaluations e ON e.submission_id = s.id AND e.judge_id = $1
       WHERE s.category_id = ANY($2::int[]) AND s.status = 'accepted'
       ORDER BY s.id ASC`,
      [judgeId, categoryIds]
    );

    return {
      assignments: assignments.rows,
      submissions: submissionsRes.rows,
    };
  }

  // Judge scores a submission
  async evaluateSubmission(
    judgeId: number,
    submissionId: number,
    data: {
      comment?: string;
      confirmed?: boolean;
      scores: { criterion_id: number; score: number }[];
    }
  ) {
    // 1. Check if submission is accepted
    const subRes = await query(
      `SELECT s.id, s.category_id, cat.contest_id 
       FROM submissions s
       JOIN categories cat ON s.category_id = cat.id
       WHERE s.id = $1 AND s.status = 'accepted'`,
      [submissionId]
    );
    if (subRes.rowCount === 0) {
      throw { statusCode: 400, message: 'Chỉ được phép chấm điểm bài thi đã được duyệt (accepted)' };
    }
    const submission = subRes.rows[0];

    // 2. Check if already evaluated and confirmed (NFR-7: Cannot change confirmed evaluation)
    const evalRes = await query(
      `SELECT id, confirmed FROM evaluations WHERE judge_id = $1 AND submission_id = $2`,
      [judgeId, submissionId]
    );

    if (evalRes.rowCount && evalRes.rows[0].confirmed) {
      throw {
        statusCode: 403,
        message: 'Đánh giá này đã được xác nhận (confirmed) và đã khóa, không thể chỉnh sửa',
      };
    }

    let evaluationId: number;
    if (evalRes.rowCount === 0) {
      const newEval = await query(
        `INSERT INTO evaluations (judge_id, submission_id, comment, confirmed)
         VALUES ($1, $2, $3, $4)
         RETURNING id`,
        [judgeId, submissionId, data.comment || null, data.confirmed || false]
      );
      evaluationId = newEval.rows[0].id;
    } else {
      evaluationId = evalRes.rows[0].id;
      await query(
        `UPDATE evaluations 
         SET comment = $1, confirmed = $2, updated_at = CURRENT_TIMESTAMP
         WHERE id = $3`,
        [data.comment || null, data.confirmed || false, evaluationId]
      );
    }

    // 3. Upsert scores
    if (data.scores && data.scores.length > 0) {
      for (const item of data.scores) {
        // Validate criterion max_score
        const critRes = await query(`SELECT max_score FROM criteria WHERE id = $1`, [item.criterion_id]);
        if (critRes.rowCount && item.score > parseFloat(critRes.rows[0].max_score)) {
          throw {
            statusCode: 400,
            message: `Điểm số (${item.score}) vượt quá thang điểm tối đa (${critRes.rows[0].max_score}) của tiêu chí`,
          };
        }

        await query(
          `INSERT INTO evaluation_scores (evaluation_id, criterion_id, score)
           VALUES ($1, $2, $3)
           ON CONFLICT (evaluation_id, criterion_id) DO UPDATE SET score = EXCLUDED.score`,
          [evaluationId, item.criterion_id, item.score]
        );
      }
    }

    await logActivity(judgeId, 'EVALUATE_SUBMISSION', 'EVALUATION', evaluationId, {
      submissionId,
      confirmed: data.confirmed,
    });

    return { evaluationId, confirmed: data.confirmed || false };
  }

  // FE11: Score Aggregation & Ranking
  async getRankings(categoryId: number) {
    const sql = `
      SELECT s.id as submission_id, s.title, s.image_path, s.thumbnail_path,
             u.name as participant_name,
             COUNT(DISTINCT e.judge_id) as judge_count,
             COALESCE(
               SUM(es.score * (c.weight / 100.0)) / NULLIF(COUNT(DISTINCT e.judge_id), 0),
               0
             ) as weighted_score
      FROM submissions s
      JOIN users u ON s.participant_id = u.id
      LEFT JOIN evaluations e ON e.submission_id = s.id AND e.confirmed = TRUE
      LEFT JOIN evaluation_scores es ON es.evaluation_id = e.id
      LEFT JOIN criteria c ON es.criterion_id = c.id
      WHERE s.category_id = $1 AND s.status = 'accepted'
      GROUP BY s.id, s.title, s.image_path, s.thumbnail_path, u.name
      ORDER BY weighted_score DESC
    `;
    const result = await query(sql, [categoryId]);
    return result.rows.map((row, index) => ({
      ...row,
      rank: index + 1,
      weighted_score: Number(parseFloat(row.weighted_score).toFixed(2)),
    }));
  }
}

export const judgingService = new JudgingService();
