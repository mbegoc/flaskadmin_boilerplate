import sys
import os

import pytest

wdir = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
if wdir not in sys.path:
    sys.path.insert(0, wdir)

from flask_demo.main import app as flask_app  # noqa: E402


@pytest.fixture
def app():
    return flask_app
