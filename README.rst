Flask Admin demo
================

Flask setup with some extension to compare with  django capabilities.

Roadmap
=======

1. configure flask-assets to collect static files
   see if I could integrate config to manage s3
2. Flask-markdown
3. setup of roles and authorizations for flask-admin
4. see the possibilities of fixtures in a django style
5. See how to activate csrf token protection
6. See how to manage related items
7. See how to manage published content - explore idea of publication table
8. See if I could contribute to flask-admin to add a FileField linked to the
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

How To Run The Tests
====================

With tox: install tox in a virtualenv or globally and run

    tox

With pytest: install pytest in a virtualenv or glabally and run

    py.test

at project root
