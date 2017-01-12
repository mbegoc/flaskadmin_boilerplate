import os

from flask import redirect, url_for, request
from flask_user import current_user
from flask_admin import Admin
from flask_admin.form import rules, ImageUploadField, SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin as BaseFileAdmin
from flask_babelex import lazy_gettext as _

from flask_demo.models import db, User, Role


media_path = os.path.join(os.path.dirname(__file__), "media")
os.makedirs(media_path, exist_ok=True)


admin = Admin(
    name=_("My app"),
    template_mode="bootstrap3",
    base_template="base.html"
)


class SecuredViewMixin:
    authorized_roles = tuple()
    form_base_class = SecureForm

    def is_accessible(self):
        return (
            current_user.is_authenticated and
            current_user.active and
            current_user.has_role(self.authorized_roles)
        )

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("admin.index"))
        else:
            return redirect(url_for('user.login', next=request.url))


class UserModelView(SecuredViewMixin, ModelView):
    authorized_roles = ("admin",)

    can_view_details = True

    form_create_rules = (
        "active",
        "username",
        "email",
        "roles",
        rules.Field("avatar"),
        "first_name",
        "last_name",
    )

    form_ajax_refs = {
        "roles": {
            "fields": ["name"],
        }
    }

    column_exclude_list = [
        "password",
        "reset_password_token",
        "email",
        "first_name",
        "last_name",
    ]

    form_excluded_columns = [
        "password",
        "reset_password_token",
        "confirmed_at",
    ]

    column_details_exclude_list = [
        "password",
        "reset_password_token",
    ]

    column_searchable_list = [
        "username",
        "email",
        "first_name",
        "last_name",
    ]

    column_filters = [
        "username",
        "email",
        "roles",
    ]

    column_editable_list = [
        "username",
        "email",
        "first_name",
        "last_name",
        "active",
        "roles",
    ]

    form_overrides = {
        "avatar": ImageUploadField,
    }

    column_labels = {
        "active": _("Active"),
        "username": _("Username"),
        "email": _("Email"),
        "avatar": _("Avatar"),
        "first_name": _("First Name"),
        "last_name": _("Last Name"),
        "confirmed_at": _("Confirmed At"),
    }

    form_args = {
        "avatar": {
            "base_path": media_path,
            "thumbnail_size": (50, 50, True),
            "endpoint": "media",
        },
    }

    form_widget_args = {
        "active": {
            "class": "",
        }
    }


class RoleModelView(SecuredViewMixin, ModelView):
    authorized_roles = ("admin",)

    can_edit = False

    form_excluded_columns = ["users"]

    column_searchable_list = [
        "name",
    ]

    column_filters = [
        "name",
    ]

    column_editable_list = [
        "name",
    ]

    column_labels = {
        "name": _("Name"),
    }


class FileAdmin(SecuredViewMixin, BaseFileAdmin):
    authorized_roles = ("admin", "editor")


admin.add_view(UserModelView(User, db.session, name=_("User")))
admin.add_view(RoleModelView(Role, db.session, name=_("Role")))
admin.add_view(FileAdmin(media_path, "/media/", name=_("Media files")))
