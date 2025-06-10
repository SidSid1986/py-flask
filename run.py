from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保表已创建
    app.run(host='0.0.0.0', port=5000, debug=True)  # 必须放在 __main__ 中！