from flask import Blueprint
from flask import request, session, render_template

mod = Blueprint('root', __name__, url_prefix='')

@mod.route('/')
@mod.route('/projects')
@mod.route('/tickets/new')
def index():
  return render_template('index.html')

@mod.route('/projects/<int:project_id>')
def tickets(project_id):
  return render_template('index.html')