import { Router } from 'express';
import { publicationController } from './publication.controller.js';
import { authenticateToken, authorizeRoles, optionalAuth } from '../../common/middleware/auth.middleware.js';

const router = Router();

// Public: view online exhibition of published contest (FE12)
router.get(
  '/exhibition/:contestId',
  optionalAuth,
  (req, res, next) => publicationController.getPublicExhibition(req, res, next)
);

// Organizer & Admin: Award management and publishing
router.post(
  '/awards',
  authenticateToken,
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => publicationController.grantAward(req, res, next)
);

router.post(
  '/publish/:contestId',
  authenticateToken,
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => publicationController.publishResults(req, res, next)
);

router.post(
  '/archive/:contestId',
  authenticateToken,
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => publicationController.archiveContest(req, res, next)
);

export const publicationRoutes = router;
