import { Router } from 'express';
import { supportController } from './support.controller.js';
import { authenticateToken, authorizeRoles } from '../../common/middleware/auth.middleware.js';

const router = Router();

router.use(authenticateToken);
router.use(authorizeRoles('organizer', 'administrator'));

router.get('/dashboard-stats', (req, res, next) => supportController.getDashboardStats(req, res, next));
router.get('/film-stock-stats', (req, res, next) => supportController.getFilmStockStats(req, res, next));

export const supportRoutes = router;
