
from dotenv import load_dotenv

load_dotenv()  # 加载当前目录的.env文件

import os
import sys
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# 初始化数据库
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False  # 禁用斜杠敏感'

    # 加载配置
    app.config.from_object('config.Config')

    # 读取环境变量（一次读取，多次使用）
    flask_env = os.getenv('FLASK_ENV')
    production_domain = os.getenv('PRODUCTION_DOMAIN', 'https://your-production-domain.com')

    # 设置日志级别
    if flask_env == 'development':
        app.logger.setLevel('DEBUG')
    else:
        app.logger.setLevel('INFO')

    # 跨域配置
    origins = []
    if flask_env == 'development':
        origins = ["http://localhost:*", "http://127.0.0.1:*"]
        app.logger.info("启用开发环境CORS配置")
    else:
        origins = [production_domain]
        app.logger.info(f"启用生产环境CORS配置: {production_domain}")

    # 全局CORS配置
    CORS(
        app,
        origins=origins,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True,
        resources={r"/api/*": {"origins": origins}}
    )

    # 打印关键配置（调试用）
    app.logger.debug("=" * 50)
    app.logger.debug("数据库连接配置:")
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri:
        try:
            db_host = db_uri.split('@')[-1].split('?')[0] if '@' in db_uri else 'unknown'
            db_user = db_uri.split('://')[1].split(':')[0] if '://' in db_uri else 'unknown'
            app.logger.debug(f"地址: {db_host}")
            app.logger.debug(f"账号: {db_user}")
        except Exception as e:
            app.logger.error(f"解析数据库URI时出错: {str(e)}")
    app.logger.debug("=" * 50)

    # 初始化数据库
    db.init_app(app)

    # 数据库连接测试
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1")).scalar()
            app.logger.info("✅ 数据库连接成功！")
        except SQLAlchemyError as e:
            app.logger.error(f"❌ 数据库连接失败！类型: {type(e).__name__}, 信息: {str(e)}")
            app.logger.error("建议检查:")
            app.logger.error("1. 确保MySQL服务正在运行")
            app.logger.error("2. 检查防火墙设置")
            app.logger.error("3. 验证用户名密码是否正确")
            sys.exit(1)

    # 注册蓝图
    from app import routes
    app.register_blueprint(routes.bp)

    app.logger.info(f"开始准备打印")
    for rule in app.url_map.iter_rules():
        app.logger.info(rule)

    # 打印所有注册的路由规则（用于调试）
    app.logger.debug("=" * 50)
    app.logger.debug("注册的路由规则:")
    for rule in app.url_map.iter_rules():
        app.logger.debug(f"  {rule.rule} -> {rule.endpoint}")
    app.logger.debug("=" * 50)

    # 确保处理OPTIONS请求
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # 全局异常处理
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, SQLAlchemyError):
            db.session.rollback()
            return jsonify({"error": "数据库操作失败", "details": str(e)}), 500
        elif isinstance(e, ValueError):
            return jsonify({"error": "参数格式错误", "details": str(e)}), 400
        else:
            app.logger.error(f"未处理异常: {str(e)}", exc_info=True)
            return jsonify({"error": "服务器内部错误", "details": "请联系管理员"}), 500

    return app