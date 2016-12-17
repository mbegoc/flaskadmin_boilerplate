#!/usr/bin/env python

from flask import render_template, Flask, url_for
from flask_script import Manager, Server
from flask_mail import Mail, email_dispatched
from flask_user import UserManager, SQLAlchemyAdapter
from flask_admin import helpers as admin_helpers
from flask_migrate import Migrate, MigrateCommand

from models import db, User
from admin import admin


app = Flask(__name__)

app.config.from_pyfile("config/default.cfg")
app.config.from_envvar("ENV_CONFIG_FILE", silent=True)

db.init_app(app)
migrate = Migrate(app, db)
user_db_adapter = SQLAlchemyAdapter(db, User)

mail = Mail(app)
user_manager = UserManager(user_db_adapter, app)
admin.init_app(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(
    host="0.0.0.0",
    port=5000,
))


@app.context_processor
def user_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for,
    )


@email_dispatched.connect
def log_message(message, app):
    """Provides console display for sent emails
    """
    if app.config.get("DEBUG", False):
        log = [message.subject, "_" * len(message.subject), message.body]
        app.logger.debug("\n".join(log))


@app.route("/")
def index():
    """Index endpoint that does nothing special for now but providing an entry
    point to app.
    """
    return render_template("index.html")


if __name__ == "__main__":
    manager.run()
