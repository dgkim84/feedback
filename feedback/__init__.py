from flask import Flask

import redis

app = Flask(__name__)
app.config.from_object('config')

db = redis.StrictRedis(host = app.config.get('REDIS_HOST', 'localhost')
    , port = app.config.get('REDIS_PORT', 6379)
    , db = app.config.get('REDIS_DB', 0))

from feedback.commons.views import mod as commonsModule
from feedback.projects.views import mod as projectsModule
from feedback.tickets.views import mod as ticketsModule

from feedback.admin.views import mod as adminModule

app.register_blueprint(adminModule)
app.register_blueprint(commonsModule)
app.register_blueprint(projectsModule)
app.register_blueprint(ticketsModule)
