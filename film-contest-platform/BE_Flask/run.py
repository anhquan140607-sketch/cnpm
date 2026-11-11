import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Film Contest Platform - Flask Clean Architecture Server running on http://127.0.0.1:{port}")
    print(f"📖 Swagger API Documentation: http://127.0.0.1:{port}/api/docs")
    app.run(host='0.0.0.0', port=port, debug=True)
