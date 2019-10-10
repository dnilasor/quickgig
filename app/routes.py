from flask import render_template
from app import app

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