from flask import render_template, flash, redirect, request, url_for, current_app
from flask_login import current_user, login_required
from app.models import User, Gig, Neighborhood, Gigtype
from app import db
from app.main.forms import EditProfileForm, GigForm, SearchForm
from app.main.tables import Results
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
  form = SearchForm()
  if form.validate_on_submit():
      if form.neighborhood_search.data == None:
          neighborhood_name = None
          neighborhood_id = None
      else:
          neighborhood_name = form.neighborhood_search.data.name
          neighborhood = Neighborhood.query.filter_by(name=neighborhood_name).first()
          neighborhood_id = neighborhood.id
      if form.type_search.data == None:
          type_name = None
          type_id = None
      else:
          type_name = form.type_search.data.name
          type = Gigtype.query.filter_by(name=type_name).first()
          type_id = type.id
      return search_results(neighborhood_id, neighborhood_name, type_id, type_name)
  return render_template('search.html', form=form)
  page = request.args.get('page', 1, type=int)
  gigs = current_user.favorite_gigs().paginate(
    page, current_app.config['GIGS_PER_PAGE'], False)
  next_url = url_for('main.index', page=gigs.next_num) \
    if gigs.has_next else None
  prev_url = url_for('main.index', page=gigs.prev_num) \
    if gigs.has_prev else None
  # return render_template('index.html', title='Home', form=form, gigs=gigs.items, next_url=next_url, prev_url=prev_url)
  return render_template('index.html', title='Home', gigs=gigs.items, next_url=next_url, prev_url=prev_url)

# language logic for later
# language = guess_language(form.gig.data)
# if language == 'UNKNOWN' or len(language) > 5:
  # language = ''
# also add to Gig def attr list below
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  form = GigForm()
  if form.validate_on_submit():
    neighborhood_name = form.neighborhood.data.name
    neighborhood = Neighborhood.query.filter_by(name=neighborhood_name).first()
    neighborhood_id = neighborhood.id
    type_name = form.type.data.name
    type = Gigtype.query.filter_by(name=type_name).first()
    type_id = type.id
    gig = Gig(detail=form.gig.data, employer=current_user, neighborhood_id=neighborhood_id, type_id=type_id)
    db.session.add(gig)
    db.session.commit()
    flash('Help is on the way! Your Gig is now live.')
    return redirect(url_for('main.create'))
  return render_template('create.html', title='Create Gig', form=form)

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

@bp.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        neighborhood_name = form.neighborhood_search.data.name
        neighborhood = Neighborhood.query.filter_by(name=neighborhood_name).first()
        neighborhood_id = neighborhood.id
        return search_results(neighborhood_id, neighborhood_name)
    return render_template('search.html', form=form)

@bp.route('/search_results')
def search_results(neighborhood_id, neighborhood_name, type_id, type_name):
    results = []
    page = request.args.get('page', 1, type=int)
    query = Gig.query
    # paginate = paginate(page, current_app.config['GIGS_PER_PAGE'], False)
    if neighborhood_id and type_id:
        query = query.filter(Gig.neighborhood_id == neighborhood_id and Gig.type_id == type_id)
    elif neighborhood_id:  query = query.filter(Gig.neighborhood_id == neighborhood_id)
    else:  query = query.filter(Gig.type_id == type_id)
    # Add more filter attributes here and then catch the error, use flash message if no filters are passed
    gigs = query.all()
    flash(_('The %(neighborhood_name)s Neighborhood has the following Gigs available:', neighborhood_name=neighborhood_name))
    return render_template('search_results.html', gigs=gigs)

@bp.route('/<id>_detail/')
def detail(id):
    gig = Gig.query.get(id)
    return render_template('gig_detail.html', gig=gig)


# Below is a better search function that returns tuples of results from a join of the Neighborhood and Gig tables.
# I think this is the best way to include Name instead of ID (or even in addition to it)
# BUT I have been unable to use it with the Table class because it doesn't accept tuples inside of tuples -
# it is looking for a simple tuple representing a database row it seems, not a join
# so to get this to work I tried not using the table and just adding an HTML table in
# the Jinja2 template "search_results.html" (see comments there for implementation detail)
# the problem with that is I couldn't figure out what the join values are actually called in the template
# so I cannot yet display the data : )

# @bp.route('/search_results')
# def search_results(neighborhood_id):
#     results = []
#     query = Gig.query
#     if neighborhood_id:
#         query = (db.session.query(Gig, Neighborhood, Gigtype).outerjoin(Neighborhood))
#     results = query.all()
#
#     # table = Results(results)
#     # table.border = True
#     return render_template('search_results.html', results=results)
