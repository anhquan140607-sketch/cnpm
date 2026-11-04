export const swaggerDocument = {
  openapi: '3.0.0',
  info: {
    title: 'Nền tảng quản lý cuộc thi nhiếp ảnh phim tích hợp AI (API)',
    version: '1.0.0',
    description: `Tài liệu REST API cho toàn bộ hệ thống Film Photography Contest Management Platform.
Bao gồm xác thực JWT, phân quyền 4 vai trò (Administrator, Organizer, Judge, Participant), quản lý cuộn phim, khung hình, nộp bài, chấm điểm và triển lãm.`,
  },
  servers: [
    {
      url: 'http://localhost:5000/api/v1',
      description: 'Local Development Server',
    },
  ],
  components: {
    securitySchemes: {
      bearerAuth: {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
        description: 'Nhập access token nhận được từ endpoint /auth/login vào đây',
      },
    },
  },
  security: [
    {
      bearerAuth: [],
    },
  ],
  paths: {
    '/auth/register': {
      post: {
        tags: ['Xác thực & Tài khoản (FE1)'],
        summary: 'Đăng ký tài khoản người tham gia (Participant)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['name', 'email', 'password'],
                properties: {
                  name: { type: 'string', example: 'Nguyễn Văn A' },
                  email: { type: 'string', example: 'nguyenvana@gmail.com' },
                  password: { type: 'string', example: 'password123' },
                  phone: { type: 'string', example: '0987654321' },
                  bio: { type: 'string', example: 'Đam mê chụp ảnh phim đường phố' },
                },
              },
            },
          },
        },
        responses: {
          201: { description: 'Đăng ký thành công' },
          409: { description: 'Email đã tồn tại' },
        },
      },
    },
    '/auth/login': {
      post: {
        tags: ['Xác thực & Tài khoản (FE1)'],
        summary: 'Đăng nhập hệ thống (Lấy Access Token & Refresh Token)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['email', 'password'],
                properties: {
                  email: { type: 'string', example: 'admin@filmcontest.vn' },
                  password: { type: 'string', example: 'password123' },
                },
              },
            },
          },
        },
        responses: {
          200: { description: 'Đăng nhập thành công' },
          401: { description: 'Sai email hoặc mật khẩu' },
        },
      },
    },
    '/auth/refresh': {
      post: {
        tags: ['Xác thực & Tài khoản (FE1)'],
        summary: 'Làm mới Access Token bằng Refresh Token',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['refreshToken'],
                properties: {
                  refreshToken: { type: 'string' },
                },
              },
            },
          },
        },
        responses: {
          200: { description: 'Làm mới token thành công' },
        },
      },
    },
    '/auth/profile': {
      get: {
        tags: ['Xác thực & Tài khoản (FE1)'],
        summary: 'Lấy thông tin tài khoản hiện tại',
        responses: {
          200: { description: 'Thành công' },
        },
      },
      put: {
        tags: ['Xác thực & Tài khoản (FE1)'],
        summary: 'Cập nhật thông tin tài khoản cá nhân',
        requestBody: {
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  phone: { type: 'string' },
                  bio: { type: 'string' },
                  avatar_url: { type: 'string' },
                },
              },
            },
          },
        },
        responses: {
          200: { description: 'Cập nhật thành công' },
        },
      },
    },
    '/system/master-data': {
      get: {
        tags: ['Hệ thống & Danh mục (FE2)'],
        summary: 'Lấy danh mục dữ liệu (film_brand, film_stock, iso, film_format, camera, lens, lab, scanner)',
        parameters: [
          {
            name: 'type',
            in: 'query',
            description: 'Lọc theo loại danh mục',
            schema: {
              type: 'string',
              enum: ['film_brand', 'film_stock', 'iso', 'film_format', 'camera', 'lens', 'lab', 'scanner'],
            },
          },
        ],
        responses: {
          200: { description: 'Thành công' },
        },
      },
      post: {
        tags: ['Hệ thống & Danh mục (FE2)'],
        summary: 'Thêm mục danh mục mới (Chỉ Administrator)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['type', 'value'],
                properties: {
                  type: { type: 'string' },
                  value: { type: 'string' },
                  description: { type: 'string' },
                },
              },
            },
          },
        },
        responses: {
          201: { description: 'Tạo thành công' },
        },
      },
    },
    '/system/activity-logs': {
      get: {
        tags: ['Hệ thống & Danh mục (FE2)'],
        summary: 'Xem nhật ký hoạt động hệ thống (Chỉ Administrator)',
        parameters: [
          { name: 'page', in: 'query', schema: { type: 'integer', default: 1 } },
          { name: 'limit', in: 'query', schema: { type: 'integer', default: 50 } },
          { name: 'entity_type', in: 'query', schema: { type: 'string' } },
        ],
        responses: {
          200: { description: 'Thành công' },
        },
      },
    },
    '/contests': {
      get: {
        tags: ['Cuộc thi & Tiêu chí (FE3, FE4)'],
        summary: 'Xem danh sách cuộc thi (Công khai)',
        parameters: [
          { name: 'status', in: 'query', schema: { type: 'string', enum: ['draft', 'open', 'closed', 'judging', 'published', 'archived'] } },
        ],
        responses: {
          200: { description: 'Thành công' },
        },
      },
      post: {
        tags: ['Cuộc thi & Tiêu chí (FE3, FE4)'],
        summary: 'Tạo cuộc thi mới (Organizer, Administrator)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['title', 'theme', 'submission_start', 'submission_end', 'judging_start', 'judging_end'],
                properties: {
                  title: { type: 'string' },
                  theme: { type: 'string' },
                  description: { type: 'string' },
                  regulations: { type: 'string' },
                  submission_start: { type: 'string', format: 'date-time' },
                  submission_end: { type: 'string', format: 'date-time' },
                  judging_start: { type: 'string', format: 'date-time' },
                  judging_end: { type: 'string', format: 'date-time' },
                },
              },
            },
          },
        },
        responses: {
          201: { description: 'Tạo cuộc thi thành công' },
        },
      },
    },
    '/contests/{id}': {
      get: {
        tags: ['Cuộc thi & Tiêu chí (FE3, FE4)'],
        summary: 'Chi tiết cuộc thi kèm các hạng mục và tiêu chí chấm',
        parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'integer' } }],
        responses: { 200: { description: 'Thành công' } },
      },
    },
    '/contests/{id}/registrations': {
      get: {
        tags: ['Ban tổ chức - Quản lý đơn đăng ký (FE5 / CNPM-138)'],
        summary: 'Organizer xem danh sách thí sinh đăng ký cuộc thi',
        parameters: [
          { name: 'id', in: 'path', required: true, schema: { type: 'integer' }, example: 1 },
          { name: 'status', in: 'query', required: false, schema: { type: 'string', enum: ['pending', 'approved', 'rejected'] } },
        ],
        responses: { 200: { description: 'Lấy danh sách đăng ký thành công' } },
      },
    },
    '/contests/registrations/{regId}/review': {
      put: {
        tags: ['Ban tổ chức - Quản lý đơn đăng ký (FE5 / CNPM-138)'],
        summary: 'Organizer duyệt hoặc từ chối đơn đăng ký tham gia (CNPM-138)',
        parameters: [
          { name: 'regId', in: 'path', required: true, schema: { type: 'integer' }, example: 1 },
        ],
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['status'],
                properties: {
                  status: { type: 'string', enum: ['approved', 'rejected'], example: 'approved' },
                  reason: { type: 'string', example: 'Đủ điều kiện thể lệ và hồ sơ hợp lệ' },
                },
              },
            },
          },
        },
        responses: { 200: { description: 'Duyệt hoặc từ chối thành công' } },
      },
    },
    '/participant/registrations': {
      post: {
        tags: ['Người tham gia - Đăng ký cuộc thi (FE5)'],
        summary: 'Đăng ký tham gia cuộc thi và hạng mục (Participant / CNPM-44)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['contest_id', 'category_id'],
                properties: {
                  contest_id: { type: 'integer', example: 1 },
                  category_id: { type: 'integer', example: 1 },
                },
              },
            },
          },
        },
        responses: {
          201: { description: 'Đăng ký tham gia cuộc thi thành công' },
          409: { description: 'Đã đăng ký hạng mục này trong cuộc thi rồi' },
        },
      },
    },
    '/participant/registrations/my': {
      get: {
        tags: ['Người tham gia - Đăng ký cuộc thi (FE5)'],
        summary: 'Xem danh sách các cuộc thi tôi đã đăng ký tham gia (Participant)',
        responses: {
          200: { description: 'Thành công' },
        },
      },
    },
    '/participant/film-rolls': {
      get: {
        tags: ['Người tham gia - Cuộn phim & Khung hình (FE6)'],
        summary: 'Xem danh sách cuộn phim của tôi (Participant)',
        responses: { 200: { description: 'Thành công' } },
      },
      post: {
        tags: ['Người tham gia - Cuộn phim & Khung hình (FE6)'],
        summary: 'Khai báo cuộn phim mới (Participant)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  roll_name: { type: 'string', example: 'Cuộn Hà Nội Thu 2026' },
                  film_brand_id: { type: 'integer', example: 1 },
                  film_stock_id: { type: 'integer', example: 1 },
                  iso_id: { type: 'integer', example: 5 },
                  film_format_id: { type: 'integer', example: 1 },
                  camera_id: { type: 'integer', example: 1 },
                  lens_id: { type: 'integer', example: 1 },
                  lab_id: { type: 'integer', example: 1 },
                  scanner_id: { type: 'integer', example: 1 },
                  scan_specs: { type: 'string', example: 'Scan TIFF 16-bit Flat' },
                },
              },
            },
          },
        },
        responses: { 201: { description: 'Tạo cuộn phim thành công' } },
      },
    },
    '/participant/submissions': {
      post: {
        tags: ['Người tham gia - Nộp bài thi (FE7)'],
        summary: 'Nộp tác phẩm dự thi gắn với khung hình cuộn phim (Participant)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['frame_id', 'category_id', 'title', 'image_path'],
                properties: {
                  frame_id: { type: 'integer' },
                  category_id: { type: 'integer' },
                  title: { type: 'string', example: 'Nắng sớm phố cổ' },
                  description: { type: 'string', example: 'Góc phố Hàng Buồm lúc 6h sáng' },
                  image_path: { type: 'string', example: 'https://storage.googleapis.com/demo/photo1.jpg' },
                  keywords: { type: 'string', example: 'hanoi, morning, street' },
                },
              },
            },
          },
        },
        responses: { 201: { description: 'Nộp bài thi thành công' } },
      },
    },
    '/participant/upload': {
      post: {
        tags: ['Người tham gia - Nộp bài thi (FE7)'],
        summary: 'Upload ảnh scan lên máy chủ lưu trữ (FE7 / CNPM-141)',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                required: ['image_data'],
                properties: {
                  filename: { type: 'string', example: 'film-scan-01.jpg' },
                  image_data: { type: 'string', example: 'data:image/jpeg;base64,/9j/4AAQSkZJRg...' },
                },
              },
            },
          },
        },
        responses: {
          201: { description: 'Upload ảnh thành công, trả về link URL' },
        },
      },
    },
    '/judging/workspace': {
      get: {
        tags: ['Chấm điểm & Xếp hạng (FE10, FE11)'],
        summary: 'Không gian chấm thi của Giám khảo (Judge)',
        responses: { 200: { description: 'Thành công' } },
      },
    },
    '/support/dashboard-stats': {
      get: {
        tags: ['Vận hành & Thống kê (FE15)'],
        summary: 'Thống kê tổng quan nền tảng (Organizer, Administrator)',
        responses: { 200: { description: 'Thành công' } },
      },
    },
  },
};
