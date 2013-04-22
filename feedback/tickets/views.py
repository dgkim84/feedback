from flask import Blueprint
from flask import request, session, make_response

from feedback.commons.utils import serialize, peek, decrease
from feedback.tickets.models import Ticket
from feedback.tickets.forms import TicketForm

mod = Blueprint('tickets', __name__, url_prefix='/api/v1/tickets')

@mod.route('/', methods=('GET','POST'))
def tickets():
  if request.method == 'GET':
    project_id = request.args.get('project_id')
    kwargs = {'num': 20, 'max_id': float(request.args.get('max_id', 'inf'))}
    index = 'connects'
    if project_id:
      kwargs['part'] = 'project'
      kwargs['project'] = project_id
    items = Ticket.all(index=index, **kwargs)
    items = Ticket.assemble_with_connects(items)
    return serialize({
      'continuation': decrease(Ticket.make_unique_index(peek(items), index)) if len(items) >= kwargs['num'] and peek(items) else None,
      'items': items
    })
  else:
    form = TicketForm(csrf_enabled=False)
    if form.validate_on_submit():
      t = Ticket(project = form.project.data
        , name = form.name.data
        , description = form.description.data
        , connects = 0)
      t.save()
      return serialize(t)
    else:
      return make_response(serialize({
        'errors': form.errors
      }), 400)

@mod.route('/<int:id>/connects', methods=('GET', 'PUT'))
def connects(id):
  op = request.args.get('op')
  if op == 'like':
    return Ticket.like(id)
  return ''

@mod.route('/<int:id>', methods=('GET','PUT','DELETE'))
def ticket(id):
  form = TicketForm(csrf_enabled=False)
  t = Ticket.get_by_id(id)
  if request.method == 'DELETE':
    t.delete()
    return serialize(t)
  if form.validate_on_submit():
    if t is not None:
      t.name = form.name.data
      t.description = form.description.data
      t.published = form.published.data
      t.save()
    return serialize(t)
  else:
    return serialize(t)