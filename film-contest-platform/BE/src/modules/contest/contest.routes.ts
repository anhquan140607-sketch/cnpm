import { Router } from 'express';
import { contestController } from './contest.controller.js';
import { authenticateToken, authorizeRoles, optionalAuth } from '../../common/middleware/auth.middleware.js';

const router = Router();

// Public: view contests and details
router.get('/', optionalAuth, (req, res, next) => contestController.listContests(req, res, next));
router.get('/:id', optionalAuth, (req, res, next) => contestController.getContestDetails(req, res, next));

// Organizer & Admin: manage contests
router.post(
  '/',
  authenticateToken,
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => contestController.createContest(req, res, next)
);

router.put(
  '/:id',
  authenticateToken,
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => contestController.updateContest(req, res, next)
);

router.post(
  '/:id/categories',
  authenticateToken,
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => contestController.addCategory(req, res, next)
);

router.post(
  '/:id/criteria',
  authenticateToken,
  authorizeRoles('organizer', 'administrator'),
  (req, res, next) => contestController.addCriterion(req, res, next)
);

// Organizer review registrations (FE5 / CNPM-138)
router.get(
  '/:id/registrations',
  optionalAuth,
  (req, res, next) => contestController.getRegistrations(req, res, next)
);

router.put(
  '/registrations/:regId/review',
  optionalAuth,
  (req, res, next) => contestController.reviewRegistration(req, res, next)
);

export const contestRoutes = router;
