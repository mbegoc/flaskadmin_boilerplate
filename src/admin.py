from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_user import current_user
from flask_admin import Admin

from models import db, User


admin = Admin(
    name="My app",
    template_mode="bootstrap3",
    base_template="base.html"
)


class SecuredModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login', next=request.url))


class UserModelView(SecuredModelView):
    column_exclude_list = ["password", "reset_password_token", "email",
                           "first_name", "last_name"]
    form_excluded_columns = ["password", "reset_password_token",
                             "confirmed_at"]
    column_details_exclude_list = ["password", "reset_password_token"]
    can_view_details = True
    column_searchable_list = ["username", "email", "first_name", "last_name"]
    column_filters = ["username", "email"]
    column_editable_list = ["username", "email", "first_name", "last_name",
                            "active"]
    form_widget_args = {
        "active": {
            "class": "",
        }
    }


admin.add_view(UserModelView(User, db.session))
