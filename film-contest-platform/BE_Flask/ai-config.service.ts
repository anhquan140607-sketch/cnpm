import { Pool } from 'pg';

export class AiConfigService {
    private db: Pool;

    constructor(dbPool: Pool) {
        this.db = dbPool;
    }

    // Lấy cấu hình ngưỡng AI hiện tại
    async getAiThresholds(): Promise<any> {
        const query = `SELECT config_key, config_value FROM system_configs WHERE config_key LIKE 'AI_THRESHOLD_%'`;
        const result = await this.db.query(query);
        return result.rows;
    }

    // Cập nhật ngưỡng cảnh báo (Ví dụ: AI_THRESHOLD_DUPLICATE = 0.85)
    async updateAiThreshold(configKey: string, newValue: number): Promise<boolean> {
        const query = `
            INSERT INTO system_configs (config_key, config_value, updated_at) 
            VALUES ($1, $2, NOW())
            ON CONFLICT (config_key) 
            DO UPDATE SET config_value = $2, updated_at = NOW();
        `;
        await this.db.query(query, [configKey, newValue.toString()]);
        return true;
    }
}
