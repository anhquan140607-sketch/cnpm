import { Router } from 'express';
import { authController } from './auth.controller.js';
import { authenticateToken, authorizeRoles } from '../../common/middleware/auth.middleware.js';

const router = Router();

// Public auth routes
router.post('/register', (req, res, next) => authController.register(req, res, next));
router.post('/login', (req, res, next) => authController.login(req, res, next));
router.post('/refresh', (req, res, next) => authController.refresh(req, res, next));

// Protected user routes
router.post('/logout', authenticateToken, (req, res, next) => authController.logout(req, res, next));
router.get('/profile', authenticateToken, (req, res, next) => authController.getProfile(req, res, next));
router.put('/profile', authenticateToken, (req, res, next) => authController.updateProfile(req, res, next));
router.post('/change-password', authenticateToken, (req, res, next) => authController.changePassword(req, res, next));

// Admin user management routes
router.get('/users', authenticateToken, authorizeRoles('administrator'), (req, res, next) =>
  authController.listUsers(req, res, next)
);
router.post('/users', authenticateToken, authorizeRoles('administrator'), (req, res, next) =>
  authController.createUserByAdmin(req, res, next)
);

export const authRoutes = router;
