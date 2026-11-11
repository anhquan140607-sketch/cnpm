import { Request, Response, NextFunction } from 'express';
import { sendError } from '../utils/response.js';

export const errorHandler = (
  err: any,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  console.error('Unhandled Server Error:', {
    message: err.message,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
    path: req.originalUrl,
    method: req.method,
  });

  const statusCode = err.statusCode || 500;
  const message = err.message || 'Lỗi hệ thống nội bộ máy chủ';
  const code = err.code || 'INTERNAL_SERVER_ERROR';

  sendError(res, message, statusCode, code, process.env.NODE_ENV === 'development' ? err.stack : undefined);
};
