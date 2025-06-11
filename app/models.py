from app import db


class Task(db.Model):
    __tablename__ = 'tasks'  # 指定表名

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Task {self.title}>'