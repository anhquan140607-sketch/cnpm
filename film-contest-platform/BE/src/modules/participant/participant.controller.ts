import { Response, NextFunction } from 'express';
import { participantService } from './participant.service.js';
import { sendSuccess, sendError } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class ParticipantController {
  // Contest Registration
  async registerContest(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { contest_id, category_id } = req.body;
      if (!contest_id || !category_id) {
        sendError(res, 'Vui lòng cung cấp mã cuộc thi và mã hạng mục', 400);
        return;
      }
      const reg = await participantService.registerContest(req.user!.id, contest_id, category_id);
      sendSuccess(res, reg, 'Đăng ký tham gia cuộc thi thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async getMyRegistrations(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const list = await participantService.getMyRegistrations(req.user!.id);
      sendSuccess(res, list, 'Lấy danh sách đăng ký thành công');
    } catch (error) {
      next(error);
    }
  }

  // Film Rolls
  async createFilmRoll(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const roll = await participantService.createFilmRoll(req.user!.id, req.body);
      sendSuccess(res, roll, 'Tạo cuộn phim mới thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async getMyFilmRolls(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const rolls = await participantService.getMyFilmRolls(req.user!.id);
      sendSuccess(res, rolls, 'Lấy danh sách cuộn phim thành công');
    } catch (error) {
      next(error);
    }
  }

  async getFilmRollDetails(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const id = parseInt(req.params.id, 10);
      const roll = await participantService.getFilmRollDetails(req.user!.id, id);
      sendSuccess(res, roll, 'Lấy chi tiết cuộn phim thành công');
    } catch (error) {
      next(error);
    }
  }

  async addFrame(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const rollId = parseInt(req.params.id, 10);
      const { frame_number } = req.body;
      if (frame_number === undefined) {
        sendError(res, 'Vui lòng cung cấp số khung hình (frame_number)', 400);
        return;
      }
      const frame = await participantService.addFrame(req.user!.id, rollId, req.body);
      sendSuccess(res, frame, 'Thêm khung hình thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  // Submissions
  async submitPhoto(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { frame_id, category_id, title, image_path } = req.body;
      if (!frame_id || !category_id || !title || !image_path) {
        sendError(res, 'Vui lòng cung cấp đầy đủ frame_id, category_id, title và image_path', 400);
        return;
      }
      const submission = await participantService.submitPhoto(req.user!.id, req.body);
      sendSuccess(res, submission, 'Nộp bài thi thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async getMySubmissions(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const submissions = await participantService.getMySubmissions(req.user!.id);
      sendSuccess(res, submissions, 'Lấy danh sách bài dự thi thành công');
    } catch (error) {
      next(error);
    }
  }
}

export const participantController = new ParticipantController();
