
import sys
import os
from dotenv import load_dotenv

# Xác định thư mục gốc BE_Flask
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Nạp biến môi trường trước khi import ứng dụng
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, BASE_DIR)

from src.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    print(f"Film Contest Platform - Flask Server running on http://127.0.0.1:{port}")
    print(f"Swagger API Documentation: http://127.0.0.1:{port}/api/docs")

    app.run(host='0.0.0.0', port=port, debug=True)
