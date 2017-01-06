Flask Admin demo
================

Flask setup with some extension to compare with  django capabilities.

Bugs to fix
===========

1. If the user is not authorized to access resources, the page enter in an
   infinite loop
2. flask-login seems to make user of babel to its translation, but it's
   flask-babelex that is implemented. See if they can be used together, or
   if we could use only one.

Roadmap
=======

1. See how to manage related items: the default with "tags" is pretty cool,
   at least for simple cases. See what are inline forms. It seems there is no
   way to popup a form create/edit linked items. In some cases, it could be
   necessary.
2. Write more tests
3. See how to manage published content - explore idea of publication table
4. implement fixtures support with flask-fixtures. It does not seem to support
   dump/load operations like django, see if an alternative exists.

Good to know for projects
=========================

1. configure flask-assets to collect static files
   see if I could integrate config to manage s3
2. Flask-markdown + markdown extension in flask admin (project dependant ?)
3. See if I could contribute to flask-admin to add a FileField linked to the
   file manager content

Interesting extensions
======================

1. Flask-restful
2. flask-celery
3. flask-classy
4. flask-fillin
5. flask-flatpages - nope
6. flask-limiter ? (!!!)
7. flask-upload
8. Flask-cache
9. Flask-fixtures

How To Run The Tests
====================

With tox: install tox in a virtualenv or globally and run

    tox

With pytest: install pytest in a virtualenv or glabally and run

    py.test

at project root
