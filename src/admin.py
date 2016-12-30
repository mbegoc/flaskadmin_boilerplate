import os

from flask import redirect, url_for, request
from flask_user import current_user
from flask_admin import Admin
from flask_admin.form import rules, ImageUploadField
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from models import db, User


media_path = os.path.join(os.path.dirname(__file__), "media")
os.makedirs(media_path, exist_ok=True)


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
    form_create_rules = ("active", "username", "email", rules.Field("avatar"),
                         "first_name", "last_name")
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
    form_overrides = {
        "avatar": ImageUploadField
    }
    form_args = {
        "avatar": {
            "base_path": media_path,
            "thumbnail_size": (50, 50, True),
            "endpoint": "media"
        }
    }
    form_widget_args = {
        "active": {
            "class": "",
        }
    }


admin.add_view(UserModelView(User, db.session))
admin.add_view(FileAdmin(media_path, "/media/", name="Media files"))
