from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from app import db
from app.models import User, Task  # 从models.py导入模型

bp = Blueprint('task_api', __name__, url_prefix='/api')

@bp.before_request
def log_request_path():
    current_app.logger.debug(f"请求路径: {request.method} {request.path}")

@bp.route('/login', methods=["POST"])
def login():
    # 打印原始请求数据（调试用）
    print("原始请求数据:", request.get_data(as_text=True))  # 查看原始JSON字符串
    print("解析后的JSON:", request.json)  # 查看解析后的字典

    username = request.json.get("username")
    password = request.json.get("password")
    print(f"登录尝试 - 用户名: {username}, 密码: {password}")  # 确认值是否正确

    if not username or not password:
        return jsonify({"msg": "用户名和密码不能为空"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        print("数据库查询结果: 用户不存在")  # 调试日志
        return jsonify({"msg": "用户名或密码错误"}), 401

    if not user.check_password(password):
        print("密码验证失败")  # 调试日志
        return jsonify({"msg": "用户名或密码错误"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@bp.route('/hello')
def hello():
    return jsonify({"message": "API服务运行正常"})

@bp.route('/tasks', methods=['GET'])
@jwt_required()  # 强制验证Token
def get_tasks():
    tasks = Task.query.order_by(Task.id).all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "必须提供name字段"}), 400

    task = Task(
        name=data['name'],
        title=data.get('title'),
        gender=data.get('gender'),
        age=data.get('age'),
        salary=data.get('salary')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@bp.route('/tasks/<int:id>', methods=['GET'])
@jwt_required()  # 强制验证Token
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data: task.name = data['name']
    if 'title' in data: task.title = data['title']
    if 'gender' in data: task.gender = data['gender']
    if 'age' in data: task.age = data['age']
    if 'salary' in data: task.salary = data['salary']
    db.session.commit()
    return jsonify(task.to_dict())

@bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204