import { query } from '../../database/db.js';

export class SupportService {
  async getDashboardStats() {
    const [
      contestsCount,
      usersCount,
      submissionsCount,
      rollsCount,
      evaluationsCount,
    ] = await Promise.all([
      query(`SELECT COUNT(*) as count FROM contests`),
      query(`SELECT role, COUNT(*) as count FROM users GROUP BY role`),
      query(`SELECT status, COUNT(*) as count FROM submissions GROUP BY status`),
      query(`SELECT COUNT(*) as count FROM film_rolls`),
      query(`SELECT COUNT(*) as count, COUNT(CASE WHEN confirmed = TRUE THEN 1 END) as confirmed_count FROM evaluations`),
    ]);

    const usersByRole = usersCount.rows.reduce((acc: any, row: any) => {
      acc[row.role] = parseInt(row.count, 10);
      return acc;
    }, {});

    const submissionsByStatus = submissionsCount.rows.reduce((acc: any, row: any) => {
      acc[row.status] = parseInt(row.count, 10);
      return acc;
    }, {});

    return {
      totalContests: parseInt(contestsCount.rows[0].count, 10),
      totalFilmRolls: parseInt(rollsCount.rows[0].count, 10),
      users: {
        total: Object.values(usersByRole).reduce((a: any, b: any) => a + b, 0),
        byRole: usersByRole,
      },
      submissions: {
        total: Object.values(submissionsByStatus).reduce((a: any, b: any) => a + b, 0),
        byStatus: submissionsByStatus,
      },
      judging: {
        totalEvaluations: parseInt(evaluationsCount.rows[0].count, 10),
        confirmedEvaluations: parseInt(evaluationsCount.rows[0].confirmed_count, 10),
      },
    };
  }

  async getFilmStockPopularity() {
    const result = await query(`
      SELECT md.value as stock_name, COUNT(fr.id) as roll_count
      FROM master_data md
      JOIN film_rolls fr ON fr.film_stock_id = md.id
      WHERE md.type = 'film_stock'
      GROUP BY md.id, md.value
      ORDER BY roll_count DESC
      LIMIT 10
    `);
    return result.rows;
  }
}

export const supportService = new SupportService();
