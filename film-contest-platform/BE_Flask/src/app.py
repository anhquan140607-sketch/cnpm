from src.create_app import create_app

app = create_app()

if __name__ == '__main__':
    # Khởi chạy server trên cổng 5000 (hoặc cổng được chỉ định)
    app.run(host='0.0.0.0', port=5000, debug=True)
