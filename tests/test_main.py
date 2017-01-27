from flask import url_for
import pytest

from flask_demo.models import User


pytestmark = pytest.mark.usefixtures("testdb")


def test_app(client):
    assert client.get("/").status_code == 200


class TestLogin:

    def test_get_login(self, client):
        response = client.get(url_for("user.login"))
        assert response.status_code == 200

    def test_login(self, client, f_users):
        response = client.post(url_for("user.login"), data={
            "username": "admin",
            "password": "ab1234CD",
        })
        assert response.status_code == 302

    def test_admin_roles(self, f_users, app):
        admin = User.query.filter(User.username == 'admin').one()
        assert admin.username == "admin"
        assert [r.name for r in admin.roles] == ["admin"]

    def test_signin(self, client):
        response = client.post(url_for("user.register"), data={
            "username": "admin",
            "password": "ab1234CD",
            "retype_password": "ab1234CD",
            "email": "email@example.com",
        })
        assert response.status_code == 302


def test_media_endpoint(app):
    rules = {r.endpoint: r.rule for r in app.url_map.iter_rules()}
    assert rules.get("media").startswith("/media/")
