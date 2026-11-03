import { Response, NextFunction } from 'express';
import { judgingService } from './judging.service.js';
import { sendSuccess, sendError } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class JudgingController {
  async assignJudge(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { judge_id, category_id, round_id } = req.body;
      if (!judge_id || !category_id || !round_id) {
        sendError(res, 'Vui lòng cung cấp judge_id, category_id và round_id', 400);
        return;
      }
      const assignment = await judgingService.assignJudge(req.user!.id, judge_id, category_id, round_id);
      sendSuccess(res, assignment, 'Phân công giám khảo thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async getWorkspace(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const workspace = await judgingService.getJudgeWorkspace(req.user!.id);
      sendSuccess(res, workspace, 'Lấy không gian chấm điểm thành công');
    } catch (error) {
      next(error);
    }
  }

  async evaluateSubmission(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const submissionId = parseInt(req.params.id, 10);
      const { comment, confirmed, scores } = req.body;
      if (!scores || !Array.isArray(scores)) {
        sendError(res, 'Vui lòng cung cấp danh sách điểm theo tiêu chí (scores)', 400);
        return;
      }
      const result = await judgingService.evaluateSubmission(req.user!.id, submissionId, {
        comment,
        confirmed,
        scores,
      });
      sendSuccess(res, result, 'Lưu kết quả đánh giá thành công');
    } catch (error) {
      next(error);
    }
  }

  async getRankings(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const categoryId = parseInt(req.params.categoryId, 10);
      const rankings = await judgingService.getRankings(categoryId);
      sendSuccess(res, rankings, 'Lấy bảng xếp hạng điểm thành công');
    } catch (error) {
      next(error);
    }
  }
}

export const judgingController = new JudgingController();
