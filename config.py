# import os
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
#
# # class Config:
# #     # SQLite 数据库路径
# #     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/database.db')
# #     SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭警告
#
# class Config:
#     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@localhost/数据库名?charset=utf8mb4'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:XuHui8238478@42.51.17.104:8899/lhk_test?charset=utf8mb4'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


import os
import sys
from dotenv import load_dotenv
from urllib.parse import quote_plus

# 加载环境变量（显式指定路径更可靠）
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

class Config:
    # 带验证的环境变量读取
    def _get_env(var_name, default=None, required=False):
        """安全读取环境变量"""
        value = os.getenv(var_name, default)
        if required and value is None:
            raise ValueError(f"必须配置环境变量: {var_name}")
        return value

    # 数据库配置（生产环境应设为required=True）
    MYSQL_HOST = _get_env('MYSQL_HOST', '42.51.17.104')
    MYSQL_PORT = int(_get_env('MYSQL_PORT', '8899'))
    MYSQL_USER = _get_env('MYSQL_USER', 'root')
    MYSQL_PASSWORD = quote_plus(_get_env('MYSQL_PASSWORD', 'XuHui8238478'))  # 密码特殊字符转义
    MYSQL_DB = _get_env('MYSQL_DB', 'lhk_test')

    # 动态构建连接字符串
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
        "?charset=utf8mb4&connect_timeout=5"  # 添加连接超时
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 环境检测（兼容新旧Flask版本）
    @property
    def ENV(self):
        return os.getenv('FLASK_ENV', 'development')

# 启动时验证配置
try:
    if Config.ENV == 'production':
        print("⚠️ 生产环境配置检查:")
        assert not Config.MYSQL_PASSWORD.startswith('XuHui'), "请修改默认密码！"
        assert 'test' not in Config.MYSQL_DB.lower(), "请使用非测试数据库！"
except AssertionError as e:
    print(f"配置错误: {str(e)}")
    sys.exit(1)