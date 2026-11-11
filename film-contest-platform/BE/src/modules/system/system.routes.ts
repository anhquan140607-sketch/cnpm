import { Router } from 'express';
import { systemController } from './system.controller.js';
import { authenticateToken, authorizeRoles } from '../../common/middleware/auth.middleware.js';

const router = Router();

// Master data reading is open to all authenticated users (and can also be used publicly by participants)
router.get('/master-data', (req, res, next) => systemController.getMasterData(req, res, next));
router.get('/master-data/:id', (req, res, next) => systemController.getMasterDataById(req, res, next));

// Admin only: create, update, delete master data
router.post(
  '/master-data',
  authenticateToken,
  authorizeRoles('administrator'),
  (req, res, next) => systemController.createMasterData(req, res, next)
);
router.put(
  '/master-data/:id',
  authenticateToken,
  authorizeRoles('administrator'),
  (req, res, next) => systemController.updateMasterData(req, res, next)
);
router.delete(
  '/master-data/:id',
  authenticateToken,
  authorizeRoles('administrator'),
  (req, res, next) => systemController.deleteMasterData(req, res, next)
);

// Admin only: Activity logs (FE2.3 & NFR-7)
router.get(
  '/activity-logs',
  authenticateToken,
  authorizeRoles('administrator'),
  (req, res, next) => systemController.getActivityLogs(req, res, next)
);

export const systemRoutes = router;
