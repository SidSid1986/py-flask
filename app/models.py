# models.py
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {'schema': 'lhk_test'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    salary = db.Column(db.Float)

    def to_dict(self):
        return {
            'name': self.name,
            'title': self.title or None,
            'gender': self.gender or None,
            'age': self.age or None,
            'salary': self.salary or None
        }