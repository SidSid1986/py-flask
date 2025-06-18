import pymysql
from pymysql.cursors import DictCursor
from flask import current_app

def get_db_connection():
    """从Flask配置获取数据库连接"""
    return pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        port=current_app.config['MYSQL_PORT'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=DictCursor
    )