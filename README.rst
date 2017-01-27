Flask Admin demo
================

Flask setup with some extension to compare to django capabilities.

Bugs to fix
===========

1. flask-login seems to make use of babel for managing its translation, but
   it's flask-babelex that is instanciated. See if they can be used together,
   or if we could use only one - fixed as a contribution to the Flask-User
   project

Roadmap
=======

1. See how to manage related items: the default with "tags" is pretty cool,
   at least for simple cases. See what are inline forms. It seems there is no
   way to popup a form create/edit linked items. In some cases, it could be
   necessary.
2. Models translations ?
3. Write more tests and comments
4. implement fixtures support with flask-fixtures.
   -> It does not seem to support dump/load operations like django, see if an
   alternative exists -> Nope.
   -> Implemented a custom db fixtures system instead.  See if it could be
   integrated to flask-fixtures.
5. Make tox tests work again. See if I can use py.test to check flake8
   compliance
6. Check the format of email (text + html) and see how to send both formats
   if necessary since it's really important to be able to deliver email as html
7. Generate the sphinx doc

Knowledge that could be good to have for actual projects
========================================================

1. configure flask-assets to collect static files
   see if I could integrate config to manage s3
2. Flask-markdown + markdown extension in flask admin (project dependant ?)
3. See if I could contribute to flask-admin to add a FileField linked to the
   file manager content
4. It would be cool to have an extension which allow to route the same url
   to a "json api" or a classical html view against the accept http field
5. See how to manage published content - explore idea of publication table

Interesting extensions
======================

1. Flask-restful
4. flask-fillin
6. flask-upload
7. Flask-cache (optional - optimization)
2. flask-celery (very optional)
3. flask-classy (very optional)
5. flask-limiter ? (!!!) (very optional AND cool)
8. flask-flatpages - nope
9. Flask-fixtures  # gave it a try, it doesn't work with py.test + sqlite
   it may be easy to make something custom with py.test fixtures and
   flask-script. Maybe it could turn as a new flask-extension or a major
   contribution to flask-fixtures.
   Roadmap to make flask-fixtures better:
   1. make it support py.test
   2. make it support sqlite (as well as postgres and mysql)
   3. implement a loaddata operation
   4. implement a dumpdata operation

How To Run The Tests
====================

With tox: install tox in a virtualenv or globally and run

    tox

With pytest: install pytest in a virtualenv or glabally and run

    py.test

at project root
