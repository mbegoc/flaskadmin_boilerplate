Flask Admin demo
================

Flask setup with some extension to compare with  django capabilities.

Roadmap
=======

1. configure flask-assets to collect static files
   see if I could integrate config to manage s3
2. Flask-markdown
3. setup of roles and authorizations for flask-admin
4. tests
5. see the possibilities of fixtures in a django style
6. See how to activate csrf token protection
7. See how to manage related items
8. See how to manage published content - explore idea of publication table
9. See if I could contribute to flask-admin to add a FileField linked to the
   file manager content

Interesting extensions
======================

Flask-restful
Flask-cache
flask-celery
flask-classy
flask-fillin
flask-flatpages - nope
flask-limiter ? (!!!)
flask-upload

How To Run The Tests
====================

With tox: install tox in a virtualenv or globally and run `tox`
