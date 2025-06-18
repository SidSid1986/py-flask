from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from app import db  # 使用已配置的db实例

# 初始化蓝图
bp = Blueprint('task_api', __name__, url_prefix='/api')

# 请求钩子：记录所有进入蓝图的请求路径
@bp.before_request
@bp.before_request
def log_request_path():
    current_app.logger.debug(f"请求路径: {request.method} {request.path}")
    current_app.logger.debug(f"完整URL: {request.url}")
    current_app.logger.debug(f"来源: {request.referrer}")

# 数据模型
class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {'schema': 'lhk_test'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(120))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title or None
        }

# 健康检查接口
@bp.route('/hello')
def hello():
    return jsonify({"message": "API服务运行正常", "database": "lhk_test.task"})

# 任务管理接口
# 修正任务路由处理函数中的日志记录
@bp.route('/tasks', methods=['GET'])
def get_tasks():

    current_app.logger.debug(f"request.path: {request.path}")
    current_app.logger.debug(f"request.url: {request.url}")
    try:
        tasks = Task.query.order_by(Task.id).all()
        current_app.logger.debug(f"查询到 {len(tasks)} 个任务")
        return jsonify([task.to_dict() for task in tasks])
    except SQLAlchemyError as e:
        current_app.logger.error(f"数据库查询错误: {str(e)}")
        return jsonify({"error": "获取任务列表失败", "details": str(e)}), 500



@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "必须提供name字段"}), 400

    try:
        task = Task(
            name=data['name'],
            title=data.get('title')
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'name' in data:
            task.name = data['name']
        if 'title' in data:
            task.title = data['title']
        db.session.commit()
        return jsonify(task.to_dict())
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500