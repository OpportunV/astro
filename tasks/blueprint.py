from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from models import Task, Tag
from forms import TaskForm
from app import db

tasks = Blueprint('tasks', __name__, template_folder='templates')


@tasks.route('/')
def index():
    if current_user.is_authenticated and current_user.is_admin:
        _tasks = Task.query.all()
    else:
        _tasks = Task.query.filter_by(is_active=True)
    return render_template('tasks/index.html', tasks=_tasks, title='Tasks')


@tasks.route('/<link>')
def task_details(link):
    task = Task.query.filter(Task.link == link).first()
    if task:
        tags = task.tags
        return render_template('tasks/task_details.html', task=task, tags=tags)
    flash('task not found', 'warning')
    return redirect(url_for('tasks.index'))


@tasks.route('/tag/<slug>')
def tag_details(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    _tasks = tag.tasks.all()
    return render_template('tasks/tag_details.html', tag=tag, tasks=_tasks)


@tasks.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        flash(f'You are not allowed to add tasks.', 'error')
        return redirect(url_for('index'))
    
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    content=form.content.data,
                    is_active=form.is_active.data,
                    author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task has been created!', 'success')
        return redirect(url_for('tasks.task_details', link=task.link))
    return render_template('tasks/new.html', title='New Task', form=form)


@tasks.route('/<link>/update', methods=['GET', 'POST'])
@login_required
def task_update(link):
    if not current_user.is_admin:
        flash(f'You are not allowed to edit tasks.', 'error')
        return redirect(url_for('index'))
    
    task = Task.query.filter(Task.link == link).first()
    
    if not task:
        flash('task not found', 'warning')
        return redirect(url_for('tasks.index'))
    
    form = TaskForm()
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        task.is_active = form.is_active.data
        db.session.commit()
        flash('Task has been updated.', 'success')
        return redirect(url_for('tasks.task_details', link=task.link))
    
    if request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.content
        form.is_active.data = task.is_active
    
    return render_template('tasks/new.html', title='Update Task', form=form)


@tasks.route('/<link>/delete', methods=['POST'])
@login_required
def task_delete(link):
    if not current_user.is_admin:
        flash(f'You are not allowed to delete tasks.', 'error')
        return redirect(url_for('index'))
    
    task = Task.query.filter(Task.link == link).first()
    
    if not task:
        flash('task not found', 'warning')
        return redirect(url_for('tasks.index'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Task has been deleted.', 'success')
    return redirect(url_for('tasks.index'))
