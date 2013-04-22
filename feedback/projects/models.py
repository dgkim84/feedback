from feedback.commons.models import Redis

class Project(Redis):
  __namespace__ = 'project:meta'
  __indexes__ = ['id']
  __partitions__ = []

  def __init__(self, *args, **kwargs):
    super(Project, self).__init__(*args, **kwargs)