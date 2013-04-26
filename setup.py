from setuptools import setup

setup(
  name='feedback',
  packages=['feedback'],
  version='0.0.1',
  description='give me a feedback',
  author='Daegeun Kim',
  author_email='dgkim84@gmail.com',
  tests_require=[
    'attest==0.6dev_20130427',
    'redismock==1.0.5'
  ],
  dependency_links=[
    'https://github.com/dahlia/attest/archive/master.tar.gz#egg=attest-0.6dev_20130427'
  ],
  test_loader='attest:auto_reporter.test_loader',
  test_suite='feedbacktests.tests',
  setup_requires=[
    'gevent==0.13.8',
    'flask==0.9',
    'Jinja2==2.6',
    'Werkzeug==0.8.3',
    'flask-wtf==0.8.3',
    'redis==2.7.2',
    'flask-assets==0.8',
    'requests==1.2.0'
  ]
)
