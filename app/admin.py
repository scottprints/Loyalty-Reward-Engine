from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import db
from app.models import Customer, Prize, SpinResult, PointsTransaction

class SecureModelView(ModelView):
    can_export = True
    column_searchable_list = ['id', 'email', 'name', 'reason']
    column_filters = ['id', 'email', 'name', 'reason']
    page_size = 50


def init_admin(app):
    admin = Admin(app, name='Loyalty Reward Admin', template_mode='bootstrap4')
    admin.add_view(SecureModelView(Customer, db.session))
    admin.add_view(SecureModelView(Prize, db.session))
    admin.add_view(SecureModelView(SpinResult, db.session))
    admin.add_view(SecureModelView(PointsTransaction, db.session)) 