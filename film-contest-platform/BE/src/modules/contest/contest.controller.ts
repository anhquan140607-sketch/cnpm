import { Response, NextFunction } from 'express';
import { contestService } from './contest.service.js';
import { sendSuccess, sendError } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class ContestController {
  async listContests(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const status = req.query.status as string;
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '20', 10);
      const result = await contestService.listContests(status, page, limit);
      sendSuccess(res, result.contests, 'Lấy danh sách cuộc thi thành công', 200, result.meta);
    } catch (error) {
      next(error);
    }
  }

  async getContestDetails(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id, 10);
      const contest = await contestService.getContestDetails(id);
      sendSuccess(res, contest, 'Lấy thông tin chi tiết cuộc thi thành công');
    } catch (error) {
      next(error);
    }
  }

  async createContest(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { title, theme, submission_start, submission_end, judging_start, judging_end } = req.body;
      if (!title || !theme || !submission_start || !submission_end || !judging_start || !judging_end) {
        sendError(res, 'Vui lòng điền đầy đủ tiêu đề, chủ đề và các mốc thời gian bắt buộc', 400);
        return;
      }
      const contest = await contestService.createContest(req.user!.id, req.body);
      sendSuccess(res, contest, 'Tạo cuộc thi thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async updateContest(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id, 10);
      const updated = await contestService.updateContest(req.user!.id, id, req.body);
      sendSuccess(res, updated, 'Cập nhật cuộc thi thành công');
    } catch (error) {
      next(error);
    }
  }

  async addCategory(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const contestId = parseInt(req.params.id, 10);
      const { name } = req.body;
      if (!name) {
        sendError(res, 'Vui lòng cung cấp tên hạng mục thi', 400);
        return;
      }
      const category = await contestService.addCategory(req.user!.id, contestId, req.body);
      sendSuccess(res, category, 'Thêm hạng mục thi thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async addCriterion(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const contestId = parseInt(req.params.id, 10);
      const { name, weight } = req.body;
      if (!name || weight === undefined) {
        sendError(res, 'Vui lòng cung cấp tên tiêu chí và trọng số (weight)', 400);
        return;
      }
      const criterion = await contestService.addCriterion(req.user!.id, contestId, req.body);
      sendSuccess(res, criterion, 'Thêm tiêu chí chấm thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  // FE5 / CNPM-138: Organizer xem danh sách và duyệt đơn đăng ký
  async getRegistrations(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const contestId = parseInt(req.params.id, 10);
      const status = req.query.status as string;
      const list = await contestService.getRegistrations(contestId, status);
      sendSuccess(res, list, 'Lấy danh sách đăng ký cuộc thi thành công');
    } catch (error) {
      next(error);
    }
  }

  async reviewRegistration(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const regId = parseInt(req.params.regId, 10);
      const { status, reason } = req.body;
      if (!status) {
        sendError(res, 'Vui lòng cung cấp trạng thái duyệt (approved hoặc rejected)', 400);
        return;
      }
      const organizerId = req.user ? req.user.id : 2; // fallback Organizer default (id=2)
      const updated = await contestService.reviewRegistration(organizerId, regId, status, reason);
      sendSuccess(res, updated, `Đã cập nhật trạng thái đơn đăng ký thành ${status}`);
    } catch (error) {
      next(error);
    }
  }
}

export const contestController = new ContestController();
