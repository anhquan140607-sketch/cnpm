import { Router } from 'express';
import { judgingController } from './judging.controller.js';
import { authenticateToken, authorizeRoles } from '../../common/middleware/auth.middleware.js';

const router = Router();

router.use(authenticateToken);

// Organizer & Admin: Assign judge & view aggregate ranking
router.post(
  '/assign',
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => judgingController.assignJudge(req, res, next)
);

router.get(
  '/rankings/:categoryId',
  authorizeRoles('organizer', 'administrator', 'judge'),
  (req, res, next) => judgingController.getRankings(req, res, next)
);

// Judge workspace & scoring
router.get(
  '/workspace',
  authorizeRoles('judge'),
  (req, res, next) => judgingController.getWorkspace(req, res, next)
);

router.post(
  '/submissions/:id/evaluate',
  authorizeRoles('judge'),
  (req, res, next) => judgingController.evaluateSubmission(req, res, next)
);

export const judgingRoutes = router;
