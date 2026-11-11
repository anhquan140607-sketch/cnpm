import { Router } from 'express';
import { verificationController } from './verification.controller.js';
import { authenticateToken, authorizeRoles } from '../../common/middleware/auth.middleware.js';

const router = Router();

router.use(authenticateToken);
router.use(authorizeRoles('organizer', 'administrator'));

router.get('/submissions', (req, res, next) => verificationController.listSubmissions(req, res, next));
router.put('/submissions/:id/verify', (req, res, next) => verificationController.verifySubmission(req, res, next));
router.get('/submissions/:id/ai-results', (req, res, next) => verificationController.getAiResults(req, res, next));

export const verificationRoutes = router;
