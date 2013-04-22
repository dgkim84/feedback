from feedback.commons.models import Redis

class Ticket(Redis):
  __namespace__ = 'ticket:meta'
  __indexes__ = ['id', 'connects']
  __partitions__ = ['project']

  def __init__(self, *args, **kwargs):
    super(Ticket, self).__init__(*args, **kwargs)

  @classmethod
  def like(cls, id):
    p = Redis.pipeline()
    p.hincrby('ticket:connects', id)
    p.hget('ticket:connects', id)
    res = p.execute()

    this = cls.get_by_id(id)
    this.connects = res[1]
    this.save()

    return res[1]

  @classmethod
  def assemble_with_connects(cls, items):
    if items:
      values = Redis.hmget('ticket:connects', [i['id'] for i in items])
      for i in range(len(values)):
        if values[i]:
          items[i]['connects'] = values[i]
        else:
          items[i]['connects'] = 0
      return items
    else:
      return items