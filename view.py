from flask import render_template, flash, redirect, url_for

from app import app
from forms import RegistrationForm, LoginForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@a.com' and form.password.data == 'pass':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        flash('Login unsuccessful. Please try again', 'danger')
    return render_template('login.html', title='Login', form=form)
