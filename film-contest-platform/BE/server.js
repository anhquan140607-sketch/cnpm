import app from './app.js';
import { config } from './config/index.js';
import { pool } from './database/db.js';
const server = app.listen(config.port, async () => {
    console.log(`================================================================`);
    console.log(`🎬 FILM CONTEST PLATFORM - BACKEND REST API SERVER RUNNING`);
    console.log(`📡 Port: http://localhost:${config.port}`);
    console.log(`📖 API Documentation (Swagger): http://localhost:${config.port}/api/docs`);
    console.log(`🩺 Health Check: http://localhost:${config.port}/api/health`);
    console.log(`⚙️  Environment: ${config.env}`);
    console.log(`================================================================`);
    try {
        const res = await pool.query('SELECT NOW()');
        console.log(`✅ Kết nối cơ sở dữ liệu PostgreSQL thành công: ${res.rows[0].now}`);
    }
    catch (dbError) {
        console.warn(`⚠️  Chưa kết nối được PostgreSQL (${config.db.host}:${config.db.port}/${config.db.database}).`);
        console.warn(`💡 Hãy kiểm tra service PostgreSQL hoặc chạy lệnh 'npm run db:init' để khởi tạo schema.`);
    }
});
const gracefulShutdown = () => {
    console.log('Shutting down server gracefully...');
    server.close(async () => {
        console.log('HTTP server closed.');
        await pool.end();
        console.log('Database pool closed.');
        process.exit(0);
    });
};
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);
