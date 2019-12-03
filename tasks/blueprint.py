from flask import Blueprint, render_template

from models import Task, Tag

tasks = Blueprint('tasks', __name__, template_folder='templates')


@tasks.route('/')
def index():
    tasks = Task.query.all()
    return render_template('tasks/index.html', tasks=tasks, title='Tasks')


@tasks.route('/<link>')
def task_details(link):
    task = Task.query.filter(Task.link == link).first()
    tags = task.tags
    return render_template('tasks/task_details.html', task=task, tags=tags)


@tasks.route('/tag/<slug>')
def tag_details(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    tasks = tag.tasks.all()
    return render_template('tasks/tag_details.html', tag=tag, tasks=tasks)
