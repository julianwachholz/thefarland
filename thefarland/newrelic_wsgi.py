"""

WSGI file with NewRelic wrapper.
To run, you must set the NEW_RELIC_LICENSE_KEY environment variable.

"""

import os

import newrelic.agent
from .wsgi import application as django_app

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

newrelic.agent.initialize(os.path.join(BASE_DIR, 'config', 'newrelic.ini'))

application = newrelic.agent.WSGIApplicationWrapper(django_app)
