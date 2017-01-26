import sys
import os
from importlib import import_module

import pytest
import yaml

wdir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
if wdir not in sys.path:
    sys.path.insert(0, wdir)

from flask_demo.main import app as flask_app  # noqa: E402
from flask_demo.main import db  # noqa: E402


@pytest.fixture
def app():
    return flask_app


for filename in os.scandir(os.path.join("flask_demo", "fixtures")):
    fixture_name = "f_{}".format(
        filename.name.replace(".", "_").rsplit("_", 1)[0])

    @pytest.fixture(name=fixture_name)
    def load_fixture():
        db.session.begin_nested()
        with open(filename.path) as fixture:
            data = yaml.load(fixture)
            for dataset in data:
                if "model" in dataset:
                    class_pkg = dataset.get("model").rsplit(".", 1)
                    Model = getattr(import_module(class_pkg[0]), class_pkg[1])
                    for row in dataset.get("records"):
                        instance = Model(**row)
                        db.session.add(instance)
                        db.session.commit()
                elif "table" in dataset:
                    class_pkg = dataset.get("table").rsplit(".", 1)
                    table = getattr(import_module(class_pkg[0]), class_pkg[1])
                    db.session.execute(table.insert(), dataset.get("records"))
        yield
        db.session.rollback()


@pytest.fixture
def testdb():
    db.create_all()
    yield db
    db.drop_all()
