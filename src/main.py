#!/usr/bin/env python

from flask import render_template

from bootstrap import app, manager


@app.route("/")
def index():
    """Index endpoint that does nothing special for now but providing an entry
    point to app.
    """
    return render_template("index.html")


if __name__ == "__main__":
    manager.run()
