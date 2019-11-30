from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, SignupForm, PasswordResetRequestForm, PasswordResetForm
from werkzeug.urls import url_parse
from datetime import datetime
from app.auth.email import send_password_reset_email
from flask_babel import _, lazy_gettext as _l

@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('auth.login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('main.index')
    return redirect(next_page)
  return render_template('auth/login.html', title='Log In', form=form)

@bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.index'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = SignupForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congrats, you are signed up!')
    return redirect(url_for('auth.login'))
  return render_template('auth/signup.html', title='Signup', form=form)

@bp.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form = PasswordResetRequestForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      send_password_reset_email(user)
    # intentionally apparently sent either way to protect user privacy
    flash(
	  _('Check your email for the instructions to reset your password'))
    return redirect(url_for('auth.login'))
  return render_template('auth/password_reset_request.html', title='Reset Password', form=form)

@bp.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  user = User.verify_password_reset_token(token)
  if not user:
    return redirect(url_for('main.index'))
  form = PasswordResetForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    db.session.commit()
    flash('Your password has been reset.')
    return redirect(url_for('auth.login'))
  return render_template('auth/password_reset.html', form=form)
