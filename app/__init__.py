from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()  # 创建数据库实例

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)  # 绑定数据库到Flask

    with app.app_context():
        db.create_all()  # 创建数据表（如果不存在）

    # 允许前端项目跨域访问（根据实际前端地址配置）
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # 假设Vue运行在8080端口

    from app import routes
    app.register_blueprint(routes.bp)

    return app