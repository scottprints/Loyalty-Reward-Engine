from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class CustomerAdmin(ModelView):
    can_export = True
    page_size = 50
    column_searchable_list = ['id', 'email']
    column_filters = ['id', 'email']

class PrizeAdmin(ModelView):
    can_export = True
    page_size = 50
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name', 'is_active']

class SpinResultAdmin(ModelView):
    can_export = True
    page_size = 50
    column_searchable_list = ['id']
    column_filters = ['id', 'spun_at']

class PointsTransactionAdmin(ModelView):
    can_export = True
    page_size = 50
    column_searchable_list = ['id', 'reason']
    column_filters = ['id', 'reason', 'amount']

def init_admin(app):
    from app import db
    from app.models import Customer, Prize, SpinResult, PointsTransaction
    admin = Admin(app, name='Loyalty Reward Admin', template_mode='bootstrap4')
    admin.add_view(CustomerAdmin(Customer, db.session))
    admin.add_view(PrizeAdmin(Prize, db.session))
    admin.add_view(SpinResultAdmin(SpinResult, db.session))
    admin.add_view(PointsTransactionAdmin(PointsTransaction, db.session)) 