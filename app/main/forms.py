from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Length, InputRequired
from wtforms.fields.html5 import DateField
from flask_babel import _, lazy_gettext as _l
from app.models import User, Gig, Neighborhood, Gigtype
from datetime import datetime


class EditProfileForm(FlaskForm):
  username = StringField(_l('Username'), validators=[DataRequired()])
  about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
  submit = SubmitField(_l('Submit'))

  def __init__(self, original_username, *args, **kwargs):
    super(EditProfileForm, self).__init__(*args, **kwargs)
    self.original_username = original_username

  def validate_username(self, username):
    if username.data != self.original_username:
      user = User.query.filter_by(username=self.username.data).first()
      if user is not None:
        raise ValidationError('Please use a different username.')

class GigForm(FlaskForm):
  gig = TextAreaField(_l('Describe your gig here'), validators=[DataRequired(), Length(min=1, max=300)])
  neighborhood = QuerySelectField(query_factory=lambda: Neighborhood.query.all(), get_label="name", allow_blank=False)
  type = QuerySelectField(query_factory=lambda: Gigtype.query.all(), get_label="name", allow_blank=False)
  #date_entry = input("Enter a date i.e. 2019,11,29")
  date = DateField('DatePicker', format='%Y-%m-%d')
  # date_entry = '2019,11,29'
  # year, month, day = map(int, date_entry.split(','))
  # date = datetime.date(year, month, day) 
  submit = SubmitField(_l('Submit'))

class SearchForm(FlaskForm):
  neighborhood_search = QuerySelectField(query_factory=lambda: Neighborhood.query.all(), get_label="name", allow_blank=True)
  type_search = QuerySelectField(query_factory=lambda: Gigtype.query.all(), get_label="name", allow_blank=True)
  #date_entry = input('Enter a date (i.e. 2017,7,1)')
  #year, month, day = map(int, date_entry.split(','))
  #date_search = datetime(year, month, day)
  submit = SubmitField(_l('Submit'))
