import { Pool } from 'pg';

export class ScoreService {
    private db: Pool;

    constructor(dbPool: Pool) {
        this.db = dbPool;
    }

    // Tổng hợp điểm cho một bài dự thi (submission_id)
    async aggregateScore(submissionId: string): Promise<any> {
        const query = `
            SELECT 
                submission_id,
                COUNT(judge_id) as total_judges,
                SUM(score) as total_score,
                AVG(score) as average_score
            FROM evaluations
            WHERE submission_id = $1 AND confirmed = true
            GROUP BY submission_id;
        `;
        
        const result = await this.db.query(query, [submissionId]);
        if (result.rows.length === 0) return null;

        const aggregated = result.rows[0];
        
        // Cập nhật lại tổng điểm vào bảng submissions
        await this.db.query(
            `UPDATE submissions SET final_score = $1 WHERE id = $2`,
            [aggregated.average_score, submissionId]
        );

        return aggregated;
    }

    // Xếp hạng tự động theo Category
    async getRankingByCategory(categoryId: string): Promise<any[]> {
        const query = `
            SELECT id, title, final_score,
            RANK() OVER (ORDER BY final_score DESC) as rank_position
            FROM submissions
            WHERE category_id = $1 AND final_score IS NOT NULL;
        `;
        const result = await this.db.query(query, [categoryId]);
        return result.rows;
    }
}
