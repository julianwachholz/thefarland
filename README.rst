##########
thefarland
##########

This is the README file for thefarland.

Quickstart
==========

You'll be able to start working on this project with the following prerequisites:

- Python 3
- Django 1.7
- ``pip`` and ``virtualenv``

You can roughly follow these simple commands to get a running application::

    $ virtualenv thefarland-env
    $ source thefarland-env/bin/activate

    # Only required if you haven't setup your project yet. Remove these lines otherwise.
    $ pip install https://www.djangoproject.com/download/1.7b1/tarball/
    $ django-admin.py startproject --template=https://github.com/julianwachholz/django-project-template/archive/master.zip -e=py,rst,html thefarland

    $ # Append basic environment variables to environment setup
    $ echo "export DEBUG=1" >> thefarland-env/bin/activate
    $ echo "export PYTHONPATH=$PWD/thefarland" >> thefarland-env/bin/activate
    $ echo "export DJANGO_SETTINGS_MODULE=thefarland.settings" >> thefarland-env/bin/activate
    $ source thefarland-env/bin/activate

    $ cd thefarland/
    $ pip install -r requirements.txt
    $ django-admin.py {migrate,runserver}

Of course, you'd want to setup a proper development environment.
Refer to the complete :doc:`docs/install` in this case.
