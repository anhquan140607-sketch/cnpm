import { Request, Response, NextFunction } from 'express';
import { authService } from './auth.service.js';
import { sendSuccess, sendError } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class AuthController {
  async register(req: Request, res: Response, next: NextFunction) {
    try {
      const { name, email, password, phone, bio } = req.body;
      if (!name || !email || !password) {
        sendError(res, 'Vui lòng cung cấp đầy đủ họ tên, email và mật khẩu', 400);
        return;
      }
      if (password.length < 6) {
        sendError(res, 'Mật khẩu phải có tối thiểu 6 ký tự', 400);
        return;
      }
      const result = await authService.register({ name, email, password, phone, bio });
      sendSuccess(res, result, 'Đăng ký tài khoản thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async login(req: Request, res: Response, next: NextFunction) {
    try {
      const { email, password } = req.body;
      if (!email || !password) {
        sendError(res, 'Vui lòng cung cấp email và mật khẩu', 400);
        return;
      }
      const ip = (req.headers['x-forwarded-for'] as string) || req.socket.remoteAddress;
      const result = await authService.login({ email, password }, ip);
      sendSuccess(res, result, 'Đăng nhập thành công');
    } catch (error) {
      next(error);
    }
  }

  async refresh(req: Request, res: Response, next: NextFunction) {
    try {
      const { refreshToken } = req.body;
      if (!refreshToken) {
        sendError(res, 'Vui lòng cung cấp refreshToken', 400);
        return;
      }
      const result = await authService.refresh(refreshToken);
      sendSuccess(res, result, 'Làm mới token thành công');
    } catch (error) {
      next(error);
    }
  }

  async logout(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { refreshToken } = req.body;
      await authService.logout(req.user!.id, refreshToken);
      sendSuccess(res, null, 'Đăng xuất thành công');
    } catch (error) {
      next(error);
    }
  }

  async getProfile(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const user = await authService.getProfile(req.user!.id);
      sendSuccess(res, user, 'Lấy thông tin người dùng thành công');
    } catch (error) {
      next(error);
    }
  }

  async updateProfile(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const updated = await authService.updateProfile(req.user!.id, req.body);
      sendSuccess(res, updated, 'Cập nhật hồ sơ thành công');
    } catch (error) {
      next(error);
    }
  }

  async changePassword(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { oldPassword, newPassword } = req.body;
      if (!oldPassword || !newPassword) {
        sendError(res, 'Vui lòng cung cấp mật khẩu cũ và mật khẩu mới', 400);
        return;
      }
      if (newPassword.length < 6) {
        sendError(res, 'Mật khẩu mới phải có tối thiểu 6 ký tự', 400);
        return;
      }
      await authService.changePassword(req.user!.id, { oldPassword, newPassword });
      sendSuccess(res, null, 'Đổi mật khẩu thành công');
    } catch (error) {
      next(error);
    }
  }

  // Admin endpoints
  async listUsers(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const role = req.query.role as string;
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '20', 10);
      const result = await authService.listUsers(role, page, limit);
      sendSuccess(res, result.users, 'Lấy danh sách người dùng thành công', 200, result.meta);
    } catch (error) {
      next(error);
    }
  }

  async createUserByAdmin(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { name, email, password, role, phone, bio } = req.body;
      if (!name || !email || !password || !role) {
        sendError(res, 'Vui lòng cung cấp họ tên, email, mật khẩu và vai trò', 400);
        return;
      }
      const user = await authService.createUserByAdmin(req.user!.id, {
        name,
        email,
        password,
        role,
        phone,
        bio,
      });
      sendSuccess(res, user, 'Tạo người dùng thành công', 201);
    } catch (error) {
      next(error);
    }
  }
}

export const authController = new AuthController();
