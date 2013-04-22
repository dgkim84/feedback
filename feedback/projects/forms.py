from flask.ext.wtf import Form
from flask.ext.wtf import TextField, IntegerField, validators

class ProjectForm(Form):
  id = IntegerField('id')
  name = TextField('name', [validators.Required()])
  description = TextField('description')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self.project = None

  def validate(self):
    rs = Form.validate(self)

    return rs