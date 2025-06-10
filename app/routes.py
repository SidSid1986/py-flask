from flask import Blueprint, jsonify
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/hello')
def hello():
    return jsonify({"message": "Hello from Flask API!"})

@bp.route('/users')
def get_users():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    return jsonify(users)