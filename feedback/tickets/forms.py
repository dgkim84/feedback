from flask.ext.wtf import Form
from flask.ext.wtf import TextField, IntegerField, FloatField, validators

import datetime, time

class TicketForm(Form):
  id = IntegerField('id')
  project = IntegerField('project', [validators.Required()])
  name = TextField('name', [validators.Required()])
  description = TextField('description', [])
  published = FloatField('published', default=time.mktime(datetime.datetime.now().timetuple()))

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self.ticket = None

  def validate(self):
    rs = Form.validate(self)

    return rs