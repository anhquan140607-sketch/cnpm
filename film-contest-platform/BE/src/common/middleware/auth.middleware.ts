import { Response, NextFunction } from 'express';
import { RequestWithUser, UserRole } from '../types/index.js';
import { verifyAccessToken } from '../utils/jwt.js';
import { sendError } from '../utils/response.js';

export const authenticateToken = (
  req: RequestWithUser,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.startsWith('Bearer ') 
    ? authHeader.split(' ')[1] 
    : null;

  if (!token) {
    sendError(res, 'Yêu cầu xác thực: Thiếu Access Token', 401, 'UNAUTHORIZED');
    return;
  }

  try {
    const decoded = verifyAccessToken(token);
    req.user = decoded;
    next();
  } catch (error: any) {
    if (error.name === 'TokenExpiredError') {
      sendError(res, 'Token đã hết hạn. Vui lòng làm mới token.', 401, 'TOKEN_EXPIRED');
      return;
    }
    sendError(res, 'Token không hợp lệ', 403, 'INVALID_TOKEN');
  }
};

export const authorizeRoles = (...allowedRoles: UserRole[]) => {
  return (req: RequestWithUser, res: Response, next: NextFunction): void => {
    if (!req.user) {
      sendError(res, 'Chưa đăng nhập', 401, 'UNAUTHORIZED');
      return;
    }

    if (!allowedRoles.includes(req.user.role)) {
      sendError(
        res,
        `Quyền truy cập bị từ chối. Vai trò '${req.user.role}' không được phép thực hiện thao tác này.`,
        403,
        'FORBIDDEN'
      );
      return;
    }

    next();
  };
};

export const optionalAuth = (
  req: RequestWithUser,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.startsWith('Bearer ') 
    ? authHeader.split(' ')[1] 
    : null;

  if (token) {
    try {
      const decoded = verifyAccessToken(token);
      req.user = decoded;
    } catch {
      // Ignored for optional auth
    }
  }
  next();
};
