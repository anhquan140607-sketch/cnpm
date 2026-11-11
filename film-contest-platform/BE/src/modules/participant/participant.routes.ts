import { Router } from 'express';
import { participantController } from './participant.controller.js';
import { authenticateToken, authorizeRoles, optionalAuth } from '../../common/middleware/auth.middleware.js';

const router = Router();

// Photo Upload (FE7 / CNPM-141 / CNPM-48) - Hỗ trợ cả authenticated và demo/test không cần token
router.post(
  '/upload',
  optionalAuth,
  (req, res, next) => participantController.uploadImage(req, res, next)
);

// Protect all other participant routes
router.use(authenticateToken);

// Contest Registration (FE5)
router.post(
  '/registrations',
  authorizeRoles('participant'),
  (req, res, next) => participantController.registerContest(req, res, next)
);
router.get(
  '/registrations/my',
  authorizeRoles('participant'),
  (req, res, next) => participantController.getMyRegistrations(req, res, next)
);

// Film Rolls & Frames (FE6)
router.post(
  '/film-rolls',
  authorizeRoles('participant'),
  (req, res, next) => participantController.createFilmRoll(req, res, next)
);
router.get(
  '/film-rolls/my',
  authorizeRoles('participant'),
  (req, res, next) => participantController.getMyFilmRolls(req, res, next)
);
router.get(
  '/film-rolls/:id',
  authorizeRoles('participant'),
  (req, res, next) => participantController.getFilmRollDetails(req, res, next)
);
router.post(
  '/film-rolls/:id/frames',
  authorizeRoles('participant'),
  (req, res, next) => participantController.addFrame(req, res, next)
);

// Photo Submission (FE7)
router.post(
  '/submissions',
  authorizeRoles('participant'),
  (req, res, next) => participantController.submitPhoto(req, res, next)
);
router.get(
  '/submissions/my',
  authorizeRoles('participant'),
  (req, res, next) => participantController.getMySubmissions(req, res, next)
);

export const participantRoutes = router;
