from flask import Blueprint
from flask import request, session

from feedback.commons.utils import serialize, peek
from feedback.projects.models import Project
from feedback.projects.forms import ProjectForm

mod = Blueprint('projects', __name__, url_prefix='/api/v1/projects')

@mod.route('/', methods=('GET',))
def projects():
  if request.method == 'GET':
    max_id = float(request.args.get('max_id', 'inf'))
    items = Project.all(max_id = max_id, num = 1000000, order='asc')
    return serialize({
      'items': items
    })

@mod.route('/<int:id>', methods=('GET','PUT'))
def project(id):
  form = ProjectForm(csrf_enabled=False)
  if form.validate_on_submit():
    p = Project.get_by_id(id)
    if p is not None:
      p.name = form.name.data
      p.description = form.description.data
      p.save()
    return serialize(p)
  else:
    p = Project.get_by_id(id)
    return serialize(p)