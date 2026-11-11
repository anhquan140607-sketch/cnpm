import { Response, NextFunction } from 'express';
import { RequestWithUser } from '../types/index.js';
import { query } from '../../database/db.js';

export const logActivity = async (
  userId: number | null,
  action: string,
  entityType: string,
  entityId?: number | null,
  details?: any,
  ipAddress?: string
) => {
  try {
    await query(
      `INSERT INTO activity_logs (user_id, action, entity_type, entity_id, details, ip_address)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [userId, action, entityType, entityId || null, details ? JSON.stringify(details) : null, ipAddress || null]
    );
  } catch (error) {
    console.error('Failed to write activity log:', error);
  }
};

export const requestLogger = (req: RequestWithUser, res: Response, next: NextFunction): void => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl} ${res.statusCode} - ${duration}ms`);
  });
  next();
};
