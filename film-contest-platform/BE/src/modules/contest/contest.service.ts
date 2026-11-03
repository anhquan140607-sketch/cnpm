import { query } from '../../database/db.js';
import { logActivity } from '../../common/middleware/logger.middleware.js';

export class ContestService {
  async listContests(status?: string, page = 1, limit = 20) {
    const offset = (page - 1) * limit;
    let sql = `
      SELECT c.*, u.name as organizer_name,
             (SELECT COUNT(*) FROM categories cat WHERE cat.contest_id = c.id) as category_count,
             (SELECT COUNT(*) FROM submissions s 
              JOIN categories cat ON s.category_id = cat.id 
              WHERE cat.contest_id = c.id) as submission_count
      FROM contests c
      LEFT JOIN users u ON c.created_by = u.id
      WHERE 1=1
    `;
    let countSql = `SELECT COUNT(*) FROM contests WHERE 1=1`;
    const params: any[] = [];

    if (status) {
      params.push(status);
      sql += ` AND c.status = $${params.length}`;
      countSql += ` AND status = $${params.length}`;
    }

    sql += ` ORDER BY c.created_at DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(limit, offset);

    const [dataRes, countRes] = await Promise.all([
      query(sql, params),
      query(countSql, params.slice(0, params.length - 2)),
    ]);

    const total = parseInt(countRes.rows[0].count, 10);
    return {
      contests: dataRes.rows,
      meta: { page, limit, total, totalPages: Math.ceil(total / limit) },
    };
  }

  async getContestDetails(id: number) {
    const contestRes = await query(
      `SELECT c.*, u.name as organizer_name, u.email as organizer_email
       FROM contests c
       LEFT JOIN users u ON c.created_by = u.id
       WHERE c.id = $1`,
      [id]
    );

    if (contestRes.rowCount === 0) {
      throw { statusCode: 404, message: 'Không tìm thấy cuộc thi' };
    }

    const contest = contestRes.rows[0];

    // Fetch categories, criteria, rounds
    const [categoriesRes, criteriaRes, roundsRes] = await Promise.all([
      query(`SELECT * FROM categories WHERE contest_id = $1 ORDER BY id ASC`, [id]),
      query(`SELECT * FROM criteria WHERE contest_id = $1 ORDER BY id ASC`, [id]),
      query(`SELECT * FROM rounds WHERE contest_id = $1 ORDER BY sequence ASC`, [id]),
    ]);

    return {
      ...contest,
      categories: categoriesRes.rows,
      criteria: criteriaRes.rows,
      rounds: roundsRes.rows,
    };
  }

  async createContest(organizerId: number, data: any) {
    const result = await query(
      `INSERT INTO contests (
        title, theme, description, regulations,
        submission_start, submission_end, judging_start, judging_end,
        status, banner_url, created_by
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
      RETURNING *`,
      [
        data.title,
        data.theme,
        data.description || null,
        data.regulations || null,
        data.submission_start,
        data.submission_end,
        data.judging_start,
        data.judging_end,
        data.status || 'draft',
        data.banner_url || null,
        organizerId,
      ]
    );

    const contest = result.rows[0];
    await logActivity(organizerId, 'CREATE_CONTEST', 'CONTEST', contest.id, { title: contest.title });
    return contest;
  }

  async updateContest(userId: number, id: number, data: any) {
    const existing = await query(`SELECT config_locked, status FROM contests WHERE id = $1`, [id]);
    if (existing.rowCount === 0) {
      throw { statusCode: 404, message: 'Không tìm thấy cuộc thi' };
    }

    if (existing.rows[0].config_locked && data.config_locked !== false) {
      throw { statusCode: 400, message: 'Cấu hình cuộc thi đã bị khóa, không thể chỉnh sửa thông số quan trọng' };
    }

    const fields: string[] = [];
    const values: any[] = [];
    let idx = 1;

    const allowedKeys = [
      'title', 'theme', 'description', 'regulations',
      'submission_start', 'submission_end', 'judging_start', 'judging_end',
      'status', 'config_locked', 'banner_url'
    ];

    for (const key of allowedKeys) {
      if (data[key] !== undefined) {
        fields.push(`${key} = $${idx++}`);
        values.push(data[key]);
      }
    }

    if (fields.length === 0) {
      return this.getContestDetails(id);
    }

    fields.push(`updated_at = CURRENT_TIMESTAMP`);
    values.push(id);

    const result = await query(
      `UPDATE contests SET ${fields.join(', ')} WHERE id = $${idx} RETURNING *`,
      values
    );

    await logActivity(userId, 'UPDATE_CONTEST', 'CONTEST', id, data);
    return result.rows[0];
  }

  // Categories
  async addCategory(userId: number, contestId: number, data: any) {
    const contest = await query(`SELECT config_locked FROM contests WHERE id = $1`, [contestId]);
    if (contest.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy cuộc thi' };
    if (contest.rows[0].config_locked) throw { statusCode: 400, message: 'Cuộc thi đã bị khóa cấu hình' };

    const result = await query(
      `INSERT INTO categories (contest_id, name, max_photos_per_participant, submission_rules, award_structure)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING *`,
      [contestId, data.name, data.max_photos_per_participant || 3, data.submission_rules || null, data.award_structure || null]
    );

    await logActivity(userId, 'ADD_CATEGORY', 'CATEGORY', result.rows[0].id, { contestId, name: data.name });
    return result.rows[0];
  }

  // Criteria (Weight verification: sum <= 100)
  async addCriterion(userId: number, contestId: number, data: any) {
    const contest = await query(`SELECT config_locked, status FROM contests WHERE id = $1`, [contestId]);
    if (contest.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy cuộc thi' };
    if (contest.rows[0].status === 'judging') throw { statusCode: 400, message: 'Cuộc thi đang ở giai đoạn chấm điểm, không thể sửa tiêu chí' };

    const currentWeights = await query(
      `SELECT COALESCE(SUM(weight), 0) as total FROM criteria WHERE contest_id = $1`,
      [contestId]
    );
    const total = parseFloat(currentWeights.rows[0].total) + parseFloat(data.weight);
    if (total > 100) {
      throw { statusCode: 400, message: `Tổng trọng số các tiêu chí không được vượt quá 100%. Hiện tại: ${currentWeights.rows[0].total}%, thêm: ${data.weight}%` };
    }

    const result = await query(
      `INSERT INTO criteria (contest_id, category_id, name, description, weight, max_score)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [contestId, data.category_id || null, data.name, data.description || null, data.weight, data.max_score || 10.0]
    );

    await logActivity(userId, 'ADD_CRITERION', 'CRITERION', result.rows[0].id, { contestId, name: data.name, weight: data.weight });
    return result.rows[0];
  }
}

export const contestService = new ContestService();
