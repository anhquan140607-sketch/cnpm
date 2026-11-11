import { query } from '../../database/db.js';
import { logActivity } from '../../common/middleware/logger.middleware.js';

export class PublicationService {
  async grantAward(
    organizerId: number,
    categoryId: number,
    submissionId: number,
    title: string,
    rank: number,
    prizeAmount?: string
  ) {
    const result = await query(
      `INSERT INTO awards (category_id, submission_id, title, rank, prize_amount)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING *`,
      [categoryId, submissionId, title, rank, prizeAmount || null]
    );

    await logActivity(organizerId, 'GRANT_AWARD', 'AWARD', result.rows[0].id, {
      submissionId,
      title,
      rank,
    });

    return result.rows[0];
  }

  async publishContestResults(organizerId: number, contestId: number) {
    const contest = await query(`SELECT status FROM contests WHERE id = $1`, [contestId]);
    if (contest.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy cuộc thi' };

    await query(`UPDATE contests SET status = 'published', updated_at = CURRENT_TIMESTAMP WHERE id = $1`, [contestId]);
    await logActivity(organizerId, 'PUBLISH_RESULTS', 'CONTEST', contestId);
    return { contestId, status: 'published' };
  }

  async getPublicExhibition(contestId: number) {
    // Only available when contest is published or archived (NFR-2)
    const contestRes = await query(`SELECT status, title, theme FROM contests WHERE id = $1`, [contestId]);
    if (contestRes.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy cuộc thi' };
    if (!['published', 'archived'].includes(contestRes.rows[0].status)) {
      throw { statusCode: 403, message: 'Cuộc thi chưa công bố kết quả triển lãm' };
    }

    const awardsRes = await query(
      `SELECT a.*, s.title as submission_title, s.image_path, s.thumbnail_path,
              u.name as author_name, cat.name as category_name
       FROM awards a
       JOIN submissions s ON a.submission_id = s.id
       JOIN users u ON s.participant_id = u.id
       JOIN categories cat ON a.category_id = cat.id
       WHERE cat.contest_id = $1
       ORDER BY a.rank ASC`,
      [contestId]
    );

    const galleryRes = await query(
      `SELECT s.id, s.title, s.image_path, s.thumbnail_path, s.keywords,
              u.name as author_name, cat.name as category_name,
              f.frame_number, f.shooting_location,
              b.value as film_brand, stk.value as film_stock
       FROM submissions s
       JOIN users u ON s.participant_id = u.id
       JOIN categories cat ON s.category_id = cat.id
       JOIN frames f ON s.frame_id = f.id
       JOIN film_rolls fr ON f.film_roll_id = fr.id
       LEFT JOIN master_data b ON fr.film_brand_id = b.id
       LEFT JOIN master_data stk ON fr.film_stock_id = stk.id
       WHERE cat.contest_id = $1 AND s.status = 'accepted'
       ORDER BY s.submitted_at DESC`,
      [contestId]
    );

    return {
      contest: contestRes.rows[0],
      awards: awardsRes.rows,
      gallery: galleryRes.rows,
    };
  }

  async archiveContest(organizerId: number, contestId: number) {
    // Snapshot all winning submissions into archive_items
    const winningSubmissions = await query(
      `SELECT s.*, u.name as participant_name, u.email as participant_email,
              cat.name as category_name, c.title as contest_title,
              a.title as award_title, a.rank as award_rank
       FROM submissions s
       JOIN awards a ON a.submission_id = s.id
       JOIN categories cat ON s.category_id = cat.id
       JOIN contests c ON cat.contest_id = c.id
       JOIN users u ON s.participant_id = u.id
       WHERE cat.contest_id = $1`,
      [contestId]
    );

    for (const sub of winningSubmissions.rows) {
      const metadata = {
        title: sub.title,
        author: sub.participant_name,
        category: sub.category_name,
        contest: sub.contest_title,
        award: sub.award_title,
        rank: sub.award_rank,
        image_path: sub.image_path,
        submitted_at: sub.submitted_at,
      };

      await query(
        `INSERT INTO archive_items (submission_id, metadata_snapshot, judging_comments)
         VALUES ($1, $2, $3)
         ON CONFLICT (submission_id) DO NOTHING`,
        [sub.id, JSON.stringify(metadata), 'Tác phẩm đoạt giải chính thức lưu trữ số']
      );
    }

    await query(`UPDATE contests SET status = 'archived', updated_at = CURRENT_TIMESTAMP WHERE id = $1`, [contestId]);
    await logActivity(organizerId, 'ARCHIVE_CONTEST', 'CONTEST', contestId);
    return { contestId, archivedCount: winningSubmissions.rowCount };
  }
}

export const publicationService = new PublicationService();
