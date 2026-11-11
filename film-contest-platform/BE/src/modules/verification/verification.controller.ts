import { Response, NextFunction } from 'express';
import { verificationService } from './verification.service.js';
import { sendSuccess, sendError } from '../../common/utils/response.js';
import { RequestWithUser } from '../../common/types/index.js';

export class VerificationController {
  async listSubmissions(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const contestId = req.query.contest_id ? parseInt(req.query.contest_id as string, 10) : undefined;
      const status = req.query.status as string;
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '20', 10);

      const result = await verificationService.listSubmissionsForVerification(contestId, status, page, limit);
      sendSuccess(res, result.submissions, 'Lấy danh sách bài kiểm tra thành công', 200, result.meta);
    } catch (error) {
      next(error);
    }
  }

  async verifySubmission(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const submissionId = parseInt(req.params.id, 10);
      const { decision, reason } = req.body;
      if (!['accepted', 'rejected', 'needs_revision'].includes(decision)) {
        sendError(res, 'Quyết định duyệt phải là accepted, rejected hoặc needs_revision', 400);
        return;
      }
      if (decision === 'rejected' && !reason) {
        sendError(res, 'Vui lòng cung cấp lý do từ chối bài dự thi', 400);
        return;
      }
      const updated = await verificationService.verifySubmission(req.user!.id, submissionId, decision, reason);
      sendSuccess(res, updated, 'Duyệt bài dự thi thành công');
    } catch (error) {
      next(error);
    }
  }

  async getAiResults(req: RequestWithUser, res: Response, next: NextFunction) {
    try {
      const submissionId = parseInt(req.params.id, 10);
      const results = await verificationService.getAiResultsForSubmission(submissionId);
      sendSuccess(res, results, 'Lấy kết quả kiểm tra AI thành công');
    } catch (error) {
      next(error);
    }
  }
}

export const verificationController = new VerificationController();
