from flask import Flask
from attest import Tests

def make_debug_app():
  app = Flask(__name__)
  app.config['TESTING'] = True
  return app

from feedbacktests import commons, commons_blueprint

tests = Tests()
tests.register(commons.tests)
tests.register(commons_blueprint.tests)
