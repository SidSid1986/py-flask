import os

basedir = os.path.abspath(os.path.dirname(__file__))


# class Config:
#     # SQLite 数据库路径
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/database.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭警告

class Config:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://用户名:密码@localhost/数据库名?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:XuHui8238478@42.51.17.104:8899/lhk_test?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
