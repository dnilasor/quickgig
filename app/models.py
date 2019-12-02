<<<<<<< HEAD
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from hashlib import md5
import jwt
from time import time
from flask import current_app


favoriters = db.Table('favoriters',
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
    if not self.is_favorite(user):
      self.favorited.append(user)

  def unfavorite(self, user):
    if self.is_favorite(user):
      self.favorited.remove(user)

  def is_favorite(self, user):
    return self.favorited.filter(
      favoriters.c.favorited_id == user.id).count() > 0

  def favorite_gigs(self):
    favorited = Gig.query.join(
      favoriters, (favoriters.c.favorited_id == Gig.user_id)).filter(
        favoriters.c.favoriter_id == self.id)
    own = Gig.query.filter_by(user_id=self.id)
    return favorited.union(own).order_by(
          Gig.timestamp.desc())

  def get_password_reset_token(self, expires_in=600):
    return jwt.encode(
      {'password_reset': self.id, 'exp': time() + expires_in},
      current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

  @staticmethod
  def verify_password_reset_token(token):
    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['password_reset']
    except:
      return
    return User.query.get(id)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))



class Gig(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  detail = db.Column(db.String(4000))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  language = db.Column(db.String(5))
  neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id'))
  neighborhood_name = db.relationship('Neighborhood', lazy='joined', uselist=False)
  start_date = db.Column(db.Date)
  type_id = db.Column(db.Integer, db.ForeignKey('gigtype.id'))
  type_name = db.relationship('Gigtype', lazy='joined', uselist=False)
  employer_email = db.relationship('User', lazy=True, uselist=False)

  def __repr__(self):
    return '<Gig {}>'.format(self.detail)



class Neighborhood(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), index=True, unique=True)

  def __repr__(self):
    return self.name

class Gigtype(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), index=True, unique=True)

  def __repr__(self):
    return self.name
=======
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from hashlib import md5
import jwt
from time import time
from flask import current_app


favoriters = db.Table('favoriters',
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
    if not self.is_favorite(user):
      self.favorited.append(user)

  def unfavorite(self, user):
    if self.is_favorite(user):
      self.favorited.remove(user)

  def is_favorite(self, user):
    return self.favorited.filter(
      favoriters.c.favorited_id == user.id).count() > 0

  def favorite_gigs(self):
    favorited = Gig.query.join(
      favoriters, (favoriters.c.favorited_id == Gig.user_id)).filter(
        favoriters.c.favoriter_id == self.id)
    own = Gig.query.filter_by(user_id=self.id)
    return favorited.union(own).order_by(
          Gig.timestamp.desc())

  def get_password_reset_token(self, expires_in=600):
    return jwt.encode(
      {'password_reset': self.id, 'exp': time() + expires_in},
      current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

  @staticmethod
  def verify_password_reset_token(token):
    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['password_reset']
    except:
      return
    return User.query.get(id)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class Gig(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  detail = db.Column(db.String(4000))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  language = db.Column(db.String(5))
  neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhood.id'))
  neighborhood_name = db.relationship('Neighborhood', lazy='joined', uselist=False)
  start_date = db.Column(db.Date)
  type_id = db.Column(db.Integer, db.ForeignKey('gigtype.id'))
  type_name = db.relationship('Gigtype', lazy='joined', uselist=False)
  employer_email = db.relationship('User', lazy=True, uselist=False)
  

  def __repr__(self):
    return '<Gig {}>'.format(self.detail)



class Neighborhood(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), index=True, unique=True)

  def __repr__(self):
    return self.name

class Gigtype(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), index=True, unique=True)

  def __repr__(self):
    return self.name
>>>>>>> some play w returning data
