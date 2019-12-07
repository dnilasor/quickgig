from flask import render_template, current_app
from app.email import send_email
from flask_babel import _, lazy_gettext as _l


def send_password_reset_email(user):
  token = user.get_password_reset_token()
  send_email(_('[QuickGig] Reset Your Password'),
    sender=current_app.config['ADMINS'][0],
    recipients=[user.email],
    text_body=render_template('email/password_reset.txt', user=user, token=token),
    html_body=render_template('email/password_reset.html', user=user, token=token))
