import { query } from '../../database/db.js';
import { logActivity } from '../../common/middleware/logger.middleware.js';

export interface MasterDataItemDto {
  type: 'film_brand' | 'film_stock' | 'iso' | 'film_format' | 'camera' | 'lens' | 'lab' | 'scanner';
  value: string;
  description?: string;
  status?: 'active' | 'inactive';
}

export class SystemService {
  async getMasterData(type?: string, activeOnly = true) {
    let sql = `SELECT id, type, value, description, status, created_at FROM master_data WHERE 1=1`;
    const params: any[] = [];

    if (type) {
      params.push(type);
      sql += ` AND type = $${params.length}`;
    }

    if (activeOnly) {
      sql += ` AND status = 'active'`;
    }

    sql += ` ORDER BY type ASC, value ASC`;
    const result = await query(sql, params);
    return result.rows;
  }

  async getMasterDataById(id: number) {
    const result = await query(
      `SELECT id, type, value, description, status, created_at FROM master_data WHERE id = $1`,
      [id]
    );
    if (result.rowCount === 0) {
      throw { statusCode: 404, message: 'Không tìm thấy bản ghi master data' };
    }
    return result.rows[0];
  }

  async createMasterData(userId: number, data: MasterDataItemDto) {
    const result = await query(
      `INSERT INTO master_data (type, value, description, status)
       VALUES ($1, $2, $3, $4)
       RETURNING id, type, value, description, status, created_at`,
      [data.type, data.value, data.description || null, data.status || 'active']
    );

    const item = result.rows[0];
    await logActivity(userId, 'CREATE_MASTER_DATA', 'MASTER_DATA', item.id, {
      type: item.type,
      value: item.value,
    });
    return item;
  }

  async updateMasterData(userId: number, id: number, data: Partial<MasterDataItemDto>) {
    const fields: string[] = [];
    const values: any[] = [];
    let idx = 1;

    if (data.value !== undefined) {
      fields.push(`value = $${idx++}`);
      values.push(data.value);
    }
    if (data.description !== undefined) {
      fields.push(`description = $${idx++}`);
      values.push(data.description);
    }
    if (data.status !== undefined) {
      fields.push(`status = $${idx++}`);
      values.push(data.status);
    }

    if (fields.length === 0) {
      return this.getMasterDataById(id);
    }

    values.push(id);
    const result = await query(
      `UPDATE master_data SET ${fields.join(', ')} WHERE id = $${idx}
       RETURNING id, type, value, description, status, created_at`,
      values
    );

    if (result.rowCount === 0) {
      throw { statusCode: 404, message: 'Không tìm thấy bản ghi master data' };
    }

    await logActivity(userId, 'UPDATE_MASTER_DATA', 'MASTER_DATA', id, data);
    return result.rows[0];
  }

  async deleteMasterData(userId: number, id: number) {
    // Check if item is used by any film_roll
    const checkUsed = await query(
      `SELECT id FROM film_rolls 
       WHERE film_brand_id = $1 OR film_stock_id = $1 OR iso_id = $1 
          OR film_format_id = $1 OR camera_id = $1 OR lens_id = $1 
          OR lab_id = $1 OR scanner_id = $1
       LIMIT 1`,
      [id]
    );

    if (checkUsed.rowCount && checkUsed.rowCount > 0) {
      // Rule FR-2.2: Cannot delete if referenced, set inactive instead
      await query(`UPDATE master_data SET status = 'inactive' WHERE id = $1`, [id]);
      await logActivity(userId, 'DEACTIVATE_MASTER_DATA', 'MASTER_DATA', id, {
        reason: 'Referenced by film_rolls - set to inactive instead of hard delete',
      });
      return { deactivated: true, message: 'Mục danh mục đang được sử dụng trong cuộn phim nên đã được chuyển sang trạng thái Ngưng hoạt động (inactive).' };
    }

    const result = await query(`DELETE FROM master_data WHERE id = $1 RETURNING id`, [id]);
    if (result.rowCount === 0) {
      throw { statusCode: 404, message: 'Không tìm thấy bản ghi master data' };
    }

    await logActivity(userId, 'DELETE_MASTER_DATA', 'MASTER_DATA', id);
    return { deleted: true, message: 'Đã xóa mục danh mục thành công' };
  }

  async getActivityLogs(page = 1, limit = 50, entityType?: string, userId?: number) {
    const offset = (page - 1) * limit;
    let sql = `
      SELECT al.id, al.user_id, u.name as user_name, u.email as user_email, u.role as user_role,
             al.action, al.entity_type, al.entity_id, al.details, al.ip_address, al.created_at
      FROM activity_logs al
      LEFT JOIN users u ON al.user_id = u.id
      WHERE 1=1
    `;
    let countSql = `SELECT COUNT(*) FROM activity_logs WHERE 1=1`;
    const params: any[] = [];

    if (entityType) {
      params.push(entityType);
      sql += ` AND al.entity_type = $${params.length}`;
      countSql += ` AND entity_type = $${params.length}`;
    }

    if (userId) {
      params.push(userId);
      sql += ` AND al.user_id = $${params.length}`;
      countSql += ` AND user_id = $${params.length}`;
    }

    sql += ` ORDER BY al.created_at DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(limit, offset);

    const [dataRes, countRes] = await Promise.all([
      query(sql, params),
      query(countSql, params.slice(0, params.length - 2)),
    ]);

    const total = parseInt(countRes.rows[0].count, 10);

    return {
      logs: dataRes.rows,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }
}

export const systemService = new SystemService();
