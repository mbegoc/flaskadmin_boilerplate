import os

from flask import redirect, url_for, request
from flask_user import current_user
from flask_admin import Admin
from flask_admin.form import rules, ImageUploadField, SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin as BaseFileAdmin
from flask_babelex import lazy_gettext as _

from flask_demo.models import db, User, Role


# default media path is at project root. This is for demo purpose and should
# probably be placed elsewhere in an actual project
media_path = os.path.join(os.path.dirname(__file__), "media")
os.makedirs(media_path, exist_ok=True)


# initialize the flask-admin module
admin = Admin(
    name=_("My app"),
    template_mode="bootstrap3",
    base_template="base.html"
)


class SecuredViewMixin:
    """This mixin provides the flask admin methods to secure admin panel. It
    need flask-user to be installed and configured and expect a user to be
    logged to grant access.
    """
    authorized_roles = tuple()
    form_base_class = SecureForm

    def is_accessible(self):
        """Check if user is authenticated and is allowed to access resource.

        Returns a boolean
        """
        return (
            current_user.is_authenticated and
            current_user.active and
            current_user.has_role(self.authorized_roles)
        )

    def inaccessible_callback(self, name, **kwargs):
        """View function to run if access is not granted.

        Returns a Flask reponse
        """
        if current_user.is_authenticated:
            return redirect(url_for("admin.index"))
        else:
            return redirect(url_for('user.login', next=request.url))


class UserModelView(SecuredViewMixin, ModelView):
    """The admin view to manage users.
    """
    # who can access and edit users
    authorized_roles = ("admin",)

    # enable the detailed read only view
    can_view_details = True

    # say which field are editable in the form and the rules to edit them
    form_create_rules = (
        "active",
        "username",
        "email",
        "roles",
        rules.Field("avatar"),
        "first_name",
        "last_name",
    )

    # ajax population of the roles field
    form_ajax_refs = {
        "roles": {
            "fields": ["name"],
        }
    }

    # hide fields from the list view
    column_exclude_list = [
        "password",
        "reset_password_token",
        "email",
        "first_name",
        "last_name",
    ]

    # hidden fields from the form
    form_excluded_columns = [
        "password",
        "reset_password_token",
        "confirmed_at",
    ]

    # hide fields from the read only view
    column_details_exclude_list = [
        "password",
        "reset_password_token",
    ]

    # which fields to consider when searching
    column_searchable_list = [
        "username",
        "email",
        "first_name",
        "last_name",
    ]

    # which columns can be filtered
    column_filters = [
        "username",
        "email",
        "roles",
    ]

    # which fields are inline editable in list view
    column_editable_list = [
        "username",
        "email",
        "first_name",
        "last_name",
        "active",
        "roles",
    ]

    # change the default field type for manage images on avatar
    form_overrides = {
        "avatar": ImageUploadField,
    }

    # set translated labels for fields
    column_labels = {
        "active": _("Active"),
        "username": _("Username"),
        "email": _("Email"),
        "avatar": _("Avatar"),
        "first_name": _("First Name"),
        "last_name": _("Last Name"),
        "confirmed_at": _("Confirmed At"),
    }

    # args to pass to the avatar field
    form_args = {
        "avatar": {
            "base_path": media_path,
            "thumbnail_size": (50, 50, True),
            "endpoint": "media",
        },
    }

    # fix a “bug” that make checkboxes as big as text fields
    form_widget_args = {
        "active": {
            "class": "",
        }
    }


class RoleModelView(SecuredViewMixin, ModelView):
    """The admin view to edit roles
    """
    # who can edit roles
    authorized_roles = ("admin",)

    # disable form (edition is made through list view)
    can_edit = False

    # we can't add users to a role. Roles can only be given to a user.
    form_excluded_columns = ["users"]

    # the name is the only meaningful field, it's the only one that is
    # accessible
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
    """Extends default FileAdmin to secure it.
    """
    authorized_roles = ("admin", "editor")


# register all the admin views
admin.add_view(UserModelView(User, db.session, name=_("User")))
admin.add_view(RoleModelView(Role, db.session, name=_("Role")))
admin.add_view(FileAdmin(media_path, "/media/", name=_("Media files")))
