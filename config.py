import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  # MAIL_SERVER = os.environ.get('MAIL_SERVER')
  # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 465
  MAIL_USE_TLS = False
  MAIL_USE_SSL = True
  MAIL_USERNAME = 'quickgig2020@gmail.com'
  MAIL_PASSWORD = 'Iamthepassword2020@'
  ADMINS = ['rosalindwhitley2019@u.northwestern.edu']
  GIGS_PER_PAGE = 10
