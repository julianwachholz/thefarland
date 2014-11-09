#######
cookeat
#######

This is the README file for cookeat.

Quickstart
==========

You'll be able to start working on this project with the following prerequisites:

- Python 3
- Django 1.7
- ``pip`` and ``virtualenv``

You can roughly follow these simple commands to get a running application::

    $ virtualenv cookeat-env
    $ source cookeat-env/bin/activate

    # Only required if you haven't setup your project yet. Remove these lines otherwise.
    $ pip install https://www.djangoproject.com/download/1.7b1/tarball/
    $ django-admin.py startproject --template=https://github.com/julianwachholz/django-project-template/archive/master.zip -e=py,rst,html cookeat

    $ # Append basic environment variables to environment setup
    $ echo "export DEBUG=1" >> cookeat-env/bin/activate
    $ echo "export PYTHONPATH=$PWD/cookeat" >> cookeat-env/bin/activate
    $ echo "export DJANGO_SETTINGS_MODULE=cookeat.settings" >> cookeat-env/bin/activate
    $ source cookeat-env/bin/activate

    $ cd cookeat/
    $ pip install -r requirements.txt
    $ django-admin.py {migrate,runserver}

Of course, you'd want to setup a proper development environment.
Refer to the complete :doc:`docs/install` in this case.
