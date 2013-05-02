#!env/bin/python
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from feedback import app

app.config['ASSETS_DEBUG'] = False
app.config['SECRET_KEY'] = 'aa'
app.config['CSRF_ENABLED'] = False

from flask.ext.assets import Environment, Bundle
assets = Environment(app)
js = Bundle('components/angular/angular.min.js',
  'components/angular/angular-sanitize.min.js',
  'components/angular/angular-cookies.min.js',
  'components/jquery/jquery-1.8.2.js',
  'components/bootstrap/js/bootstrap.min.js',
  'components/require/require.js',
  output='gen/all.js')
assets.register('js_all', js)

