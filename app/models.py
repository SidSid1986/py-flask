from app import db

class Task(db.Model):  # 继承 db.Model 表示这是一个数据库模型
    id = db.Column(db.Integer, primary_key=True)      # 主键ID
    title = db.Column(db.String(100), nullable=False)  # 任务标题（非空）
    done = db.Column(db.Boolean, default=False)        # 完成状态（默认为False）

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done
        }