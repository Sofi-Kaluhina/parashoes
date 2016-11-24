# coding=utf8

from flask_admin import Admin

from admin import app, db_session
from admin.security import MyAdminIndexView
from admin.views import (
    UserView, CatalogUserTypeView, ProductPhotoView,
    AttributeView, AttributeValueView, ProductView
)


admin = Admin(app, 'BUlavka', index_view=MyAdminIndexView(), base_template='my_master.html')
admin.add_view(UserView(db_session))
admin.add_view(CatalogUserTypeView(db_session))
admin.add_view(AttributeView(db_session))
admin.add_view(AttributeValueView(db_session))
admin.add_view(ProductPhotoView(db_session))
admin.add_view(ProductView(db_session))
