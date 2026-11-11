import { query } from '../../database/db.js';
import { logActivity } from '../../common/middleware/logger.middleware.js';

export class ParticipantService {
  // FE5: Contest Registration
  async registerContest(participantId: number, contestId: number, categoryId: number) {
    // Check contest status & deadline
    const contestRes = await query(
      `SELECT status, submission_start, submission_end FROM contests WHERE id = $1`,
      [contestId]
    );
    if (contestRes.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy cuộc thi' };
    const contest = contestRes.rows[0];

    if (contest.status !== 'open') {
      throw { statusCode: 400, message: 'Cuộc thi hiện không mở nhận đăng ký' };
    }
    const now = new Date();
    if (now > new Date(contest.submission_end)) {
      throw { statusCode: 400, message: 'Đã hết hạn nộp bài và đăng ký tham gia' };
    }

    // Check category belongs to contest
    const catRes = await query(
      `SELECT id FROM categories WHERE id = $1 AND contest_id = $2`,
      [categoryId, contestId]
    );
    if (catRes.rowCount === 0) {
      throw { statusCode: 400, message: 'Hạng mục không thuộc cuộc thi này' };
    }

    try {
      const result = await query(
        `INSERT INTO registrations (participant_id, contest_id, category_id, status)
         VALUES ($1, $2, $3, 'approved')
         RETURNING *`,
        [participantId, contestId, categoryId]
      );
      await logActivity(participantId, 'REGISTER_CONTEST', 'REGISTRATION', result.rows[0].id, { contestId, categoryId });
      return result.rows[0];
    } catch (err: any) {
      if (err.code === '23505') {
        throw { statusCode: 409, message: 'Bạn đã đăng ký hạng mục này trong cuộc thi rồi' };
      }
      throw err;
    }
  }

  async getMyRegistrations(participantId: number) {
    const result = await query(
      `SELECT r.*, c.title as contest_title, c.theme as contest_theme, c.status as contest_status,
              cat.name as category_name
       FROM registrations r
       JOIN contests c ON r.contest_id = c.id
       JOIN categories cat ON r.category_id = cat.id
       WHERE r.participant_id = $1
       ORDER BY r.created_at DESC`,
      [participantId]
    );
    return result.rows;
  }

  // FE6: Film Roll Management
  async createFilmRoll(participantId: number, data: any) {
    const result = await query(
      `INSERT INTO film_rolls (
        participant_id, roll_name, film_brand_id, film_stock_id, iso_id,
        film_format_id, camera_id, lens_id, lab_id, scanner_id, scan_specs, notes
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
      RETURNING *`,
      [
        participantId,
        data.roll_name || 'Cuộn phim mới',
        data.film_brand_id || null,
        data.film_stock_id || null,
        data.iso_id || null,
        data.film_format_id || null,
        data.camera_id || null,
        data.lens_id || null,
        data.lab_id || null,
        data.scanner_id || null,
        data.scan_specs || null,
        data.notes || null,
      ]
    );

    const roll = result.rows[0];
    await logActivity(participantId, 'CREATE_FILM_ROLL', 'FILM_ROLL', roll.id, { roll_name: roll.roll_name });
    return roll;
  }

  async getMyFilmRolls(participantId: number) {
    const result = await query(
      `SELECT fr.*,
              b.value as film_brand, s.value as film_stock, iso.value as iso,
              fmt.value as film_format, cam.value as camera, lens.value as lens,
              lab.value as lab, sc.value as scanner,
              (SELECT COUNT(*) FROM frames f WHERE f.film_roll_id = fr.id) as frame_count
       FROM film_rolls fr
       LEFT JOIN master_data b ON fr.film_brand_id = b.id
       LEFT JOIN master_data s ON fr.film_stock_id = s.id
       LEFT JOIN master_data iso ON fr.iso_id = iso.id
       LEFT JOIN master_data fmt ON fr.film_format_id = fmt.id
       LEFT JOIN master_data cam ON fr.camera_id = cam.id
       LEFT JOIN master_data lens ON fr.lens_id = lens.id
       LEFT JOIN master_data lab ON fr.lab_id = lab.id
       LEFT JOIN master_data sc ON fr.scanner_id = sc.id
       WHERE fr.participant_id = $1
       ORDER BY fr.created_at DESC`,
      [participantId]
    );
    return result.rows;
  }

  async getFilmRollDetails(participantId: number, rollId: number) {
    const rollRes = await query(
      `SELECT fr.*,
              b.value as film_brand, s.value as film_stock, iso.value as iso,
              fmt.value as film_format, cam.value as camera, lens.value as lens,
              lab.value as lab, sc.value as scanner
       FROM film_rolls fr
       LEFT JOIN master_data b ON fr.film_brand_id = b.id
       LEFT JOIN master_data s ON fr.film_stock_id = s.id
       LEFT JOIN master_data iso ON fr.iso_id = iso.id
       LEFT JOIN master_data fmt ON fr.film_format_id = fmt.id
       LEFT JOIN master_data cam ON fr.camera_id = cam.id
       LEFT JOIN master_data lens ON fr.lens_id = lens.id
       LEFT JOIN master_data lab ON fr.lab_id = lab.id
       LEFT JOIN master_data sc ON fr.scanner_id = sc.id
       WHERE fr.id = $1 AND fr.participant_id = $2`,
      [rollId, participantId]
    );

    if (rollRes.rowCount === 0) {
      throw { statusCode: 404, message: 'Không tìm thấy cuộn phim' };
    }

    const framesRes = await query(
      `SELECT f.*, 
              (SELECT id FROM submissions s WHERE s.frame_id = f.id LIMIT 1) as submission_id
       FROM frames f WHERE f.film_roll_id = $1
       ORDER BY f.frame_number ASC`,
      [rollId]
    );

    return { ...rollRes.rows[0], frames: framesRes.rows };
  }

  // Frame Management
  async addFrame(participantId: number, rollId: number, data: any) {
    const rollCheck = await query(`SELECT id FROM film_rolls WHERE id = $1 AND participant_id = $2`, [rollId, participantId]);
    if (rollCheck.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy cuộn phim' };

    try {
      const result = await query(
        `INSERT INTO frames (film_roll_id, frame_number, shooting_location, shooting_date, shutter_speed, aperture, notes)
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         RETURNING *`,
        [
          rollId,
          data.frame_number,
          data.shooting_location || null,
          data.shooting_date || null,
          data.shutter_speed || null,
          data.aperture || null,
          data.notes || null,
        ]
      );
      return result.rows[0];
    } catch (err: any) {
      if (err.code === '23505') {
        throw { statusCode: 409, message: `Khung hình số ${data.frame_number} đã tồn tại trong cuộn phim này` };
      }
      throw err;
    }
  }

  // FE7: Photograph Submission
  async submitPhoto(participantId: number, data: any) {
    // 1. Check frame belongs to user
    const frameRes = await query(
      `SELECT f.id, fr.participant_id FROM frames f
       JOIN film_rolls fr ON f.film_roll_id = fr.id
       WHERE f.id = $1`,
      [data.frame_id]
    );
    if (frameRes.rowCount === 0 || frameRes.rows[0].participant_id !== participantId) {
      throw { statusCode: 403, message: 'Khung hình không hợp lệ hoặc không thuộc quyền sở hữu của bạn' };
    }

    // 2. Check category & contest
    const catRes = await query(
      `SELECT cat.id, cat.max_photos_per_participant, c.id as contest_id, c.status, c.submission_end
       FROM categories cat
       JOIN contests c ON cat.contest_id = c.id
       WHERE cat.id = $1`,
      [data.category_id]
    );
    if (catRes.rowCount === 0) throw { statusCode: 404, message: 'Không tìm thấy hạng mục thi' };
    const cat = catRes.rows[0];

    if (cat.status !== 'open') {
      throw { statusCode: 400, message: 'Cuộc thi hiện không mở nhận bài dự thi' };
    }
    if (new Date() > new Date(cat.submission_end)) {
      throw { statusCode: 400, message: 'Thời hạn nộp bài đã kết thúc' };
    }

    // 3. Check quota: max_photos_per_participant (FR-7.3)
    const existingSubmissions = await query(
      `SELECT COUNT(*) FROM submissions 
       WHERE category_id = $1 AND participant_id = $2 AND status != 'withdrawn'`,
      [data.category_id, participantId]
    );
    const count = parseInt(existingSubmissions.rows[0].count, 10);
    if (count >= cat.max_photos_per_participant) {
      throw {
        statusCode: 400,
        message: `Bạn đã đạt giới hạn nộp ảnh cho hạng mục này (${cat.max_photos_per_participant} ảnh)`,
      };
    }

    // 4. Create submission
    const result = await query(
      `INSERT INTO submissions (
        frame_id, category_id, participant_id, title, description,
        image_path, thumbnail_path, negative_ref_path, keywords, status
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'submitted')
      RETURNING *`,
      [
        data.frame_id,
        data.category_id,
        participantId,
        data.title,
        data.description || null,
        data.image_path,
        data.thumbnail_path || data.image_path,
        data.negative_ref_path || null,
        data.keywords || null,
      ]
    );

    const submission = result.rows[0];
    await logActivity(participantId, 'SUBMIT_PHOTO', 'SUBMISSION', submission.id, {
      title: submission.title,
      category_id: data.category_id,
    });

    return submission;
  }

  async getMySubmissions(participantId: number) {
    const result = await query(
      `SELECT s.*, cat.name as category_name, c.title as contest_title, c.status as contest_status,
              f.frame_number, f.shooting_location, fr.roll_name
       FROM submissions s
       JOIN categories cat ON s.category_id = cat.id
       JOIN contests c ON cat.contest_id = c.id
       JOIN frames f ON s.frame_id = f.id
       JOIN film_rolls fr ON f.film_roll_id = fr.id
       WHERE s.participant_id = $1
       ORDER BY s.submitted_at DESC`,
      [participantId]
    );
    return result.rows;
  }

  // FE7 / CNPM-141: Image Upload to Storage
  async uploadImage(participantId: number, filename: string, base64Content: string) {
    const fs = await import('fs');
    const path = await import('path');
    const uploadsDir = path.resolve(process.cwd(), 'uploads');
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir, { recursive: true });
    }

    const matches = base64Content.match(/^data:image\/([a-zA-Z0-9+.-]+);base64,(.+)$/);
    let ext = 'jpg';
    let dataBuffer: Buffer;

    if (matches && matches.length === 3) {
      ext = matches[1].replace('jpeg', 'jpg');
      dataBuffer = Buffer.from(matches[2], 'base64');
    } else {
      dataBuffer = Buffer.from(base64Content, 'base64');
    }

    const cleanFilename = `scan-${Date.now()}-${Math.floor(Math.random() * 10000)}.${ext}`;
    const filePath = path.join(uploadsDir, cleanFilename);
    fs.writeFileSync(filePath, dataBuffer);

    const fileUrl = `http://localhost:${process.env.PORT || 5000}/uploads/${cleanFilename}`;
    await logActivity(participantId, 'UPLOAD_IMAGE', 'IMAGE', null, { filename: cleanFilename, size: dataBuffer.length });

    return {
      url: fileUrl,
      filename: cleanFilename,
      size: dataBuffer.length,
      mimeType: `image/${ext}`,
    };
  }
}

export const participantService = new ParticipantService();
