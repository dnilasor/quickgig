from flask_admin.contrib.sqla import ModelView
from app.models import User, Gig, Neighborhood, Gigtype
from app import db
# Add views to app_admin

def add_admin_views():
    from . import app_admin
    app_admin.add_view(ModelView(User, db.session))
    app_admin.add_view(ModelView(Neighborhood, db.session))
    app_admin.add_view(ModelView(Gig, db.session))
    app_admin.add_view(ModelView(Gigtype, db.session))
