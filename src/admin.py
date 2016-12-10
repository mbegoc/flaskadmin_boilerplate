from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user
from flask_admin import Admin

from models import db, User


admin = Admin(name="Flask", template_mode="bootstrap3")


class SecuredModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login', next=request.url))


admin.add_view(SecuredModelView(User, db.session))
