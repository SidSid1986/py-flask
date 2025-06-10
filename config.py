import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLite 数据库路径
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭警告