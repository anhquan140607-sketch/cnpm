import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env file
dotenv.config();

export const config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '5000', 10),
  apiPrefix: process.env.API_PREFIX || '/api/v1',
  
  db: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD || 'postgres',
    database: process.env.DB_NAME || 'film_contest_db',
  },
  
  jwt: {
    secret: process.env.JWT_SECRET || 'fallback_secret_film_contest_key_2026',
    expiresIn: process.env.JWT_EXPIRES_IN || '1d',
    refreshSecret: process.env.JWT_REFRESH_SECRET || 'fallback_refresh_film_contest_key_2026',
    refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d',
  },
  
  cors: {
    origin: process.env.CORS_ORIGIN || '*',
  },
};
