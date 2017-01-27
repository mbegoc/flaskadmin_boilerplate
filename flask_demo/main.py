#!/usr/bin/env python

import sys
import os

wdir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
if wdir not in sys.path:
    sys.path.insert(0, wdir)

from flask import (render_template,  # noqa: E402
                   Flask,
                   url_for,
                   send_from_directory,
                   request)
from flask_script import Manager, Server  # noqa: E402
from flask_mail import Mail, email_dispatched  # noqa: E402
from flask_user import UserManager, SQLAlchemyAdapter  # noqa: E402
from flask_admin import helpers as admin_helpers  # noqa: E402
from flask_migrate import Migrate, MigrateCommand  # noqa: E402
from flask_assets import Environment as FlaskAssets  # noqa: E402
from flask_babelex import Babel  # noqa: E402

from flask_demo.models import db, User  # noqa: E402
from flask_demo.admin import admin, media_path  # noqa: E402


# create the app and load config
app = Flask(__name__)
app.config.from_pyfile("config/default.cfg")
app.config.from_envvar("ENV_CONFIG_FILE", silent=True)

# enable database
db.init_app(app)
migrate = Migrate(app, db)
user_db_adapter = SQLAlchemyAdapter(db, User)

# activate utilities extensions
mail = Mail(app)
user_manager = UserManager(user_db_adapter, app)
admin.init_app(app)

# prepare assats to be served
assets = FlaskAssets(app)
assets.register("css", app.config.get("CSS_BUNDLE"))
# assets.register("js", app.config.get("JS_BUNDLE"))

# instanciate script manager and register commands
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(
    host="0.0.0.0",
    port=5000,
))

# instanciate and prepare babel for translation
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(["fr", "en"])


# provide a template context for flask-admin
@app.context_processor
def user_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for,
    )


# make email to be displayed to console in debug
@email_dispatched.connect
def log_message(message, app):
    """Provides console display for sent emails
    """
    if app.config.get("DEBUG", False):
        log = [message.subject, "_" * len(message.subject), message.body]
        app.logger.debug("\n".join(log))


# main route
@app.route("/")
def index():
    """Index endpoint that does nothing special for now but providing an entry
    point to app.
    """
    return render_template("index.html")


# serve media files (i.e. those that are uploaded though admin and are not in
# static folder)
@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(media_path, filename)


if __name__ == "__main__":
    manager.run()
