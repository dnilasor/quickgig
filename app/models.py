from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login
from hashlib import md5


favoriters = db.Table('favorites',
  db.Column('favoriter_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('favorited_id', db.Integer, db.ForeignKey('user.id'))
  )

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  gigs = db.relationship('Gig', backref='employer', lazy='dynamic')
  about_me = db.Column(db.String(140))
  first_name = db.Column(db.String(40))
  last_name = db.Column(db.String(40))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  favorited = db.relationship(
    'User', secondary=favoriters,
	primaryjoin=(favoriters.c.favoriter_id == id),
    secondaryjoin=(favoriters.c.favorited_id == id),
    backref=db.backref('favoriters', lazy='dynamic'), lazy='dynamic')
  
  def __repr__(self):
    return '<User {}>'.format(self.username)
	
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
	
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)	
	
  def favorite(self, user):
    if not self.is_favorited(user):
      self.favorited.append(user)
  
  def unfavorite(self, user):
    if self.is_favorited(user):
      self.favorited.remove(user)

  def is_favorited(self, user):
    return self.favorited.filter(
      favoriters.c.favorited_id == user.id).count() > 0

  def favorite_gigs(self):
    favorited = Gig.query.join(
      favoriters, (favoriters.c.favorited_id == Gig.user_id.filter(
        favoriters.c.favoriter_id == self.id)
    own = Gig.query.filter_by(user_id=self.id)
    return favorited.union(own).order_by(
          Gig.timestamp.desc())
	
@login.user_loader
def load_user(id):
  return User.query.get(int(id))
	
class Gig(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  detail = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
  def __repr__(self):
    return '<Gig {}>'.format(self.detail)
	
