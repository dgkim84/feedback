from flask import Blueprint
from flask import request, session, render_template, make_response

from feedback.commons.utils import serialize, peek, decrease
from feedback.projects.models import Project
from feedback.projects.forms import ProjectForm
from feedback.tickets.models import Ticket

mod = Blueprint('admin', __name__, url_prefix='/admin')

@mod.route('/projects/new')
@mod.route('/statistics')
def index():
  return render_template('admin.html')

@mod.route('/projects', methods=('GET', 'POST'))
def projects():
  if request.method == 'GET':
    return render_template('admin.html', projects = Project.all())
  elif request.method == 'POST':
    form = ProjectForm()
    if form.validate_on_submit():
      p = Project(name = form.name.data
        , description = form.description.data)
      p.save()
      return serialize(p)
    else:
      return make_response(serialize({
        'errors': form.errors
      }), 400)