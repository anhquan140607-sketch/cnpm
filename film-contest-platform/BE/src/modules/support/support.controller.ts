import { Response, NextFunction } from 'express';
import { supportService } from './support.service.js';
import { sendSuccess } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class SupportController {
  async getDashboardStats(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const stats = await supportService.getDashboardStats();
      sendSuccess(res, stats, 'Lấy thống kê hệ thống thành công');
    } catch (error) {
      next(error);
    }
  }

  async getFilmStockStats(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const stats = await supportService.getFilmStockPopularity();
      sendSuccess(res, stats, 'Lấy thống kê dòng phim phổ biến thành công');
    } catch (error) {
      next(error);
    }
  }
}

export const supportController = new SupportController();
