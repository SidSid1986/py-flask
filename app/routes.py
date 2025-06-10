from flask import Blueprint, request, jsonify
from app.models import Task
from app import db
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/hello')
def hello():
    return jsonify({"message": "Hello from Flask API!"})

@bp.route('/users')
def get_users():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    return jsonify(users)
##########################################################
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204


@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)  # 找不到任务则返回404
    data = request.get_json()

    # 更新字段（根据前端传递的JSON动态更新）
    if 'title' in data:
        task.title = data['title']
    if 'done' in data:
        task.done = data['done']

    db.session.commit()
    return jsonify(task.to_dict())