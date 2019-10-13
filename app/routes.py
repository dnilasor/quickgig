from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'Dnilasor'}
  gigs = [
    {
	  'employer': {'username': 'ManagerJane'},
	  'detail': 'Come help me sell hip air plants in Logan Square!'
	},
	{
	  'employer': {'username': 'MustMoveNow'},
	  'detail': '$20/hr to help me gtf out of my boyfriends house in Evanston. Must be strong!'
	}
  ]
  return render_template('index.html', title='Home', user=user, gigs=gigs)
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(
      form.username.data, form.remember_me.data))
    return redirect(url_for('index'))
  return render_template('login.html', title='Log In', form=form)