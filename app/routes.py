# 导入必要的Flask模块和组件
from flask import Blueprint, request, jsonify  # Blueprint用于路由分组，request处理请求数据，jsonify返回JSON响应
from app.models import Task  # 从模型文件导入Task数据模型
from app import db  # 导入SQLAlchemy数据库实例

# 创建一个名为'api'的蓝图，所有路由都会自动添加'/api'前缀
bp = Blueprint('api', __name__, url_prefix='/api')

# 测试接口 - 返回简单的欢迎消息
@bp.route('/hello')
def hello():
    return jsonify({"message": "Hello from Flask API!"})  # 返回JSON格式的欢迎消息

# 模拟用户数据接口 - 返回静态用户列表
@bp.route('/users')
def get_users():
    # 硬编码的用户数据（实际项目应该从数据库获取）
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    return jsonify(users)  # 将用户列表转为JSON响应

##########################################################
# 任务管理系统的CRUD接口
##########################################################

# 获取所有任务 - GET请求
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    # 查询数据库获取所有任务记录
    tasks = Task.query.all()
    # 将每个任务对象转为字典格式，然后整个列表转为JSON响应
    return jsonify([task.to_dict() for task in tasks])

# 创建新任务 - POST请求
@bp.route('/tasks', methods=['POST'])
def add_task():
    # 获取前端发送的JSON数据
    data = request.get_json()
    # 创建新任务实例（只使用title字段，done默认为False）
    task = Task(title=data['title'])
    # 将新任务添加到数据库会话
    db.session.add(task)
    # 提交会话，将数据写入数据库
    db.session.commit()
    # 返回创建成功的响应（201状态码），包含创建的任务数据
    return jsonify(task.to_dict()), 201

# 删除任务 - DELETE请求
@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    # 根据ID查找任务，如果不存在则自动返回404
    task = Task.query.get_or_404(id)
    # 将任务标记为待删除
    db.session.delete(task)
    # 提交删除操作到数据库
    db.session.commit()
    # 返回空内容，204状态码表示成功但无内容返回
    return '', 204

# 更新任务 - PUT请求
@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    # 根据ID查找任务，不存在则返回404
    task = Task.query.get_or_404(id)
    # 获取前端发送的更新数据
    data = request.get_json()

    # 只更新前端提供的字段（安全做法：不假定所有字段都存在）
    if 'title' in data:  # 如果提供了title字段
        task.title = data['title']  # 更新标题
    if 'done' in data:  # 如果提供了done字段
        task.done = data['done']  # 更新完成状态

    # 提交变更到数据库
    db.session.commit()
    # 返回更新后的任务数据
    return jsonify(task.to_dict())