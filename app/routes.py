from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Gig
from app import app, db
from app.forms import LoginForm, SignupForm, EditProfileForm, GigForm
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required

def index():
  form = GigForm()
  if form.validate_on_submit():
    gig = Gig(detail=form.gig.data, employer=current_user)
    db.session.add(gig)
    db.session.commit()
    flash('Help is on the way! Your Gig is now live.')
    return redirect(url_for('index'))
  page = request.args.get('page', 1, type=int)
  gigs = current_user.favorite_gigs().paginate(
    page, app.config['GIGS_PER_PAGE'], False)
  next_url = url_for('index', page=gigs.next_num) \
    if gigs.has_next else None
  prev_url = url_for('index', page=gigs.prev_num) \
    if gigs.has_prev else None
  return render_template('index.html', title='Home', form=form, gigs=gigs.items, next_url=next_url, prev_url=prev_url)
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Log In', form=form)
  
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))  


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = SignupForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congrats, you are signed up!')
    return redirect(url_for('login'))
  return render_template('signup.html', title='Signup', form=form)
  
@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  gigs = user.gigs.order_by(Gig.timestamp.desc()).paginate(
    page, app.config['GIGS_PER_PAGE'], False)
  next_url = url_for('user', username=user.username, page=gigs.next_num) \
    if gigs.has_next else None
  prev_url = url_for('user', username=user.username, page=gigs.prev_num) \
    if gigs.has_prev else None
  return render_template('user.html', user=user, gigs=gigs.items, next_url=next_url, prev_url=prev_url)
  
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm(current_user.username)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved')
    return redirect(url_for('edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Profile', form=form)
  
@app.route('/favorite/<username>')
@login_required
def favorite(username):
  user = User.query.filter_by(username=username).first()
  if user is None:
    flash('User {} not found.'.format(username))
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot favorite yourself. Your gigs will appear in your favorites automatically.')
    return redirect(url_for('user', username=username))
  current_user.favorite(user)
  db.session.commit()
  flash('{} is in your favorites!'.format(username))
  return redirect(url_for('user', username=username))
  
@app.route('/unfavorite/<username>')
@login_required
def unfavorite(username):
  user = User.query.filter_by(username=username).first()
  if user is None:
    flash('User {} not found.'.format(username))
    return redirect(url_for('index'))
  if user == current_user:
    flash('You cannot unfavorite yourself!')
    return redirect(url_for('user', username=username))
  current_user.unfavorite(user)
  db.session.commit()
  flash('{} has been removed from your favorites.'.format(username))
  return redirect(url_for('user', username=username))
  
@app.route('/explore')
@login_required
def explore():
  page = request.args.get('page', 1, type=int)
  gigs = Gig.query.order_by(Gig.timestamp.desc()).paginate(
    page, app.config['GIGS_PER_PAGE'], False)
  next_url = url_for('explore', page=gigs.next_num) \
    if gigs.has_next else None
  prev_url = url_for('explore', page=gigs.prev_num) \
    if gigs.has_prev else None
  return render_template('index.html', title='Explore', gigs=gigs.items, next_url=next_url, prev_url=prev_url)
  
@app.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = PasswordResetRequestForm()
  if form.validate_on_submit()
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      send_password_reset_email(user)
    flash('Check your email for the instructions to reset your password')
    return redirect(url_for('login'))
   return render_template('password_reset_request.html', title='Reset Password', form=form)
  
  
