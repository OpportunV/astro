from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from app import app, bcrypt, db


@app.route('/')
def index():
    return render_template('index.html', title='Main Page')
