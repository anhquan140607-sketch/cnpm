import express, { Application, Request, Response } from 'express';
import cors from 'cors';
import swaggerUi from 'swagger-ui-express';
import { config } from './config/index.js';
import { requestLogger } from './common/middleware/logger.middleware.js';
import { errorHandler } from './common/middleware/error.middleware.js';
import { sendSuccess, sendError } from './common/utils/response.js';
import { swaggerDocument } from './docs/swagger.js';

// Import Modular Routes
import { authRoutes } from './modules/auth/auth.routes.js';
import { systemRoutes } from './modules/system/system.routes.js';
import { contestRoutes } from './modules/contest/contest.routes.js';
import { participantRoutes } from './modules/participant/participant.routes.js';
import { verificationRoutes } from './modules/verification/verification.routes.js';
import { judgingRoutes } from './modules/judging/judging.routes.js';
import { publicationRoutes } from './modules/publication/publication.routes.js';
import { supportRoutes } from './modules/support/support.routes.js';

const app: Application = express();

// Standard middlewares
app.use(cors({ origin: config.cors.origin, credentials: true }));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(requestLogger);

// Swagger Documentation UI
app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Health check endpoint
app.get('/api/health', (req: Request, res: Response) => {
  sendSuccess(res, { status: 'healthy', timestamp: new Date().toISOString() }, 'Hệ thống hoạt động bình thường');
});

// Mount Modular Routes under API prefix
const prefix = config.apiPrefix;
app.use(`${prefix}/auth`, authRoutes);
app.use(`${prefix}/system`, systemRoutes);
app.use(`${prefix}/contests`, contestRoutes);
app.use(`${prefix}/participant`, participantRoutes);
app.use(`${prefix}/verification`, verificationRoutes);
app.use(`${prefix}/judging`, judgingRoutes);
app.use(`${prefix}/publication`, publicationRoutes);
app.use(`${prefix}/support`, supportRoutes);

// 404 Not Found Handler
app.use('*', (req: Request, res: Response) => {
  sendError(res, `Đường dẫn '${req.originalUrl}' không tồn tại trên máy chủ`, 404, 'NOT_FOUND');
});

// Global Error Handler Middleware
app.use(errorHandler);

export default app;
