from flask import render_template, flash, redirect, request, url_for, current_app
from flask_login import current_user, login_required
from app.models import User, Gig
from app import db
from app.main.forms import EditProfileForm, GigForm, GigSearchForm
from datetime import datetime
from guess_language import guess_language
from app.main import bp
from flask_babel import _, lazy_gettext as _l

@bp.before_app_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  search = GigSearchForm()
  if request.method == 'POST':
    return search_results(search)
  page = request.args.get('page', 1, type=int)
  gigs = current_user.favorite_gigs().paginate(
    page, current_app.config['GIGS_PER_PAGE'], False)
  next_url = url_for('main.index', page=gigs.next_num) \
    if gigs.has_next else None
  prev_url = url_for('main.index', page=gigs.prev_num) \
    if gigs.has_prev else None
  return render_template('index.html', title='Home', form=search, gigs=gigs.items, next_url=next_url, prev_url=prev_url)
  
@bp.route('/results')
def search_results(search):
  results = []
  search_string = search.data['search']
  
  if search.data['search'] == '':
    results = db_session.query(Neighborhood).all()
	
  if not results:
    flash('No results found!')
    return redirect(url_for('main.index'))
  else:
    #display results
    return render_template('results.html', results=results)

@bp.route('/create', methods=['GET', 'POST'])
@login_required 
def create():
  form = GigForm()
  if form.validate_on_submit():
    language = guess_language(form.gig.data)
    if language == 'UNKNOWN' or len(language) > 5:
      language = ''
    gig = Gig(detail=form.gig.data, employer=current_user, language=language)
    db.session.add(gig)
    db.session.commit()
    flash('Help is on the way! Your Gig is now live.')
    return redirect(url_for('main.index'))
	
@bp.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  gigs = user.gigs.order_by(Gig.timestamp.desc()).paginate(
    page, current_app.config['GIGS_PER_PAGE'], False)
  next_url = url_for('main.user', username=user.username, page=gigs.next_num) \
    if gigs.has_next else None
  prev_url = url_for('main.user', username=user.username, page=gigs.prev_num) \
    if gigs.has_prev else None
  return render_template('user.html', user=user, gigs=gigs.items, next_url=next_url, prev_url=prev_url)
  
@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm(current_user.username)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved')
    return redirect(url_for('main.edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Your Profile', form=form)
  
@bp.route('/favorite/<username>')
@login_required
def favorite(username):
  user = User.query.filter_by(username=username).first()
  if user is None:
    flash(_('User %(username)s not found.', username=username))
    return redirect(url_for('main.index'))
  if user == current_user:
    flash(_('You cannot favorite yourself. Your gigs will appear in your favorites automatically.'))
    return redirect(url_for('main.user', username=username))
  current_user.favorite(user)
  db.session.commit()
  flash(_('%(username)s is in your favorites!', username=username))
  return redirect(url_for('main.user', username=username))
  
@bp.route('/unfavorite/<username>')
@login_required
def unfavorite(username):
  user = User.query.filter_by(username=username).first()
  if user is None:
    flash(_('User %(username)s not found.', username=username))
    return redirect(url_for('main.index'))
  if user == current_user:
    flash('You cannot unfavorite yourself!')
    return redirect(url_for('main.user', username=username))
  current_user.unfavorite(user)
  db.session.commit()
  flash(_('User %(username)s has been removed from your favorites.', username=username))
  return redirect(url_for('main.user', username=username))
  
@bp.route('/explore')
@login_required
def explore():
  page = request.args.get('page', 1, type=int)
  gigs = Gig.query.order_by(Gig.timestamp.desc()).paginate(
    page, current_app.config['GIGS_PER_PAGE'], False)
  next_url = url_for('main.explore', page=gigs.next_num) \
    if gigs.has_next else None
  prev_url = url_for('main.explore', page=gigs.prev_num) \
    if gigs.has_prev else None
  return render_template('index.html', title='Explore', gigs=gigs.items, next_url=next_url, prev_url=prev_url)
