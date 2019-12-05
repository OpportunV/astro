import re
from datetime import datetime

from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


task_tags = db.Table('post_tags',
                     db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    @property
    def is_admin(self):
        return self.id == 1

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    link = db.Column(db.String(120), unique=True)
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_added = datetime.now()
        self.link = str(int(self.date_added.timestamp() * 1e6))

    tags = db.relationship('Tag', secondary=task_tags, backref=db.backref('tasks', lazy='dynamic'))
    
    def __repr__(self):
        return f"Task('{self.title}', '{self.date_added}')"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = re.sub(r'[^\w+]', '-', self.name)
    
    def __repr__(self):
        return f"Tag('{self.id}', '{self.name}', '{self.slug}')"
