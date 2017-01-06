from flask_user import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


roles_users = db.Table(
    'roles_users',
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # User authentication information
    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(255),
        nullable=False,
        server_default=''
    )

    reset_password_token = db.Column(
        db.String(100),
        nullable=False,
        server_default=''
    )

    # User email information
    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    avatar = db.Column(
        db.String(200),
        nullable=True,
    )

    confirmed_at = db.Column(
        db.DateTime()
    )

    # User information
    active = db.Column(
        'is_active',
        db.Boolean(),
        nullable=False,
        server_default='0'
    )

    first_name = db.Column(
        db.String(100),
        nullable=False,
        server_default=''
    )

    last_name = db.Column(
        db.String(100),
        nullable=False,
        server_default=''
    )

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def has_role(self, roles):
        against_roles = set(roles)
        user_roles = set([r.name for r in self.roles])
        return bool(user_roles.intersection(against_roles))


class Role(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    def __str__(self):
        return self.name
