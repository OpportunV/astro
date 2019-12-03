from flask import Blueprint, render_template

tasks = Blueprint('unix', __name__, template_folder='templates')


@tasks.route('/')
def index():
    return render_template('unix/index.html')
