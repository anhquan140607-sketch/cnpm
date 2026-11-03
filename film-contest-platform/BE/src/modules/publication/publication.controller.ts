import { Response, NextFunction } from 'express';
import { publicationService } from './publication.service.js';
import { sendSuccess, sendError } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class PublicationController {
  async grantAward(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const { category_id, submission_id, title, rank, prize_amount } = req.body;
      if (!category_id || !submission_id || !title || rank === undefined) {
        sendError(res, 'Vui lòng cung cấp category_id, submission_id, title và rank', 400);
        return;
      }
      const award = await publicationService.grantAward(
        req.user!.id,
        category_id,
        submission_id,
        title,
        rank,
        prize_amount
      );
      sendSuccess(res, award, 'Trao giải thưởng thành công', 201);
    } catch (error) {
      next(error);
    }
  }

  async publishResults(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const contestId = parseInt(req.params.contestId, 10);
      const result = await publicationService.publishContestResults(req.user!.id, contestId);
      sendSuccess(res, result, 'Công bố kết quả cuộc thi thành công');
    } catch (error) {
      next(error);
    }
  }

  async getPublicExhibition(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const contestId = parseInt(req.params.contestId, 10);
      const exhibition = await publicationService.getPublicExhibition(contestId);
      sendSuccess(res, exhibition, 'Lấy triển lãm trực tuyến thành công');
    } catch (error) {
      next(error);
    }
  }

  async archiveContest(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const contestId = parseInt(req.params.contestId, 10);
      const result = await publicationService.archiveContest(req.user!.id, contestId);
      sendSuccess(res, result, 'Lưu trữ số cuộc thi thành công');
    } catch (error) {
      next(error);
    }
  }
}

export const publicationController = new PublicationController();
