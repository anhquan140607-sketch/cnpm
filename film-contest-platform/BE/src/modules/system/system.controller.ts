import { Response, NextFunction } from 'express';
import { systemService } from './system.service.js';
import { sendSuccess, sendError } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class SystemController {
  async getMasterData(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const type = req.query.type as string;
      const activeOnly = req.query.all !== 'true';
      const items = await systemService.getMasterData(type, activeOnly);
      sendSuccess(res, items, 'Lấy danh mục thành công');
    } catch (error) {
      next(error);
    }
  }

  async getMasterDataById(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id, 10);
      const item = await systemService.getMasterDataById(id);
      sendSuccess(res, item, 'Lấy chi tiết mục thành công');
    } catch (error) {
      next(error);
    }
  }

  async createMasterData(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { type, value, description, status } = req.body;
      if (!type || !value) {
        sendError(res, 'Vui lòng cung cấp loại danh mục (type) và giá trị (value)', 400);
        return;
      }
      const item = await systemService.createMasterData(req.user!.id, {
        type,
        value,
        description,
        status,
      });
      sendSuccess(res, item, 'Thêm mới danh mục thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async updateMasterData(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id, 10);
      const updated = await systemService.updateMasterData(req.user!.id, id, req.body);
      sendSuccess(res, updated, 'Cập nhật danh mục thành công');
    } catch (error) {
      next(error);
    }
  }

  async deleteMasterData(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id, 10);
      const result = await systemService.deleteMasterData(req.user!.id, id);
      sendSuccess(res, result, result.message);
    } catch (error) {
      next(error);
    }
  }

  async getActivityLogs(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '50', 10);
      const entityType = req.query.entity_type as string;
      const userId = req.query.user_id ? parseInt(req.query.user_id as string, 10) : undefined;

      const result = await systemService.getActivityLogs(page, limit, entityType, userId);
      sendSuccess(res, result.logs, 'Lấy nhật ký hoạt động thành công', 200, result.meta);
    } catch (error) {
      next(error);
    }
  }
}

export const systemController = new SystemController();
