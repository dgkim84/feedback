from feedback.commons.models import Redis

import json

def peek(collection):
  if collection:
    return collection[len(collection) - 1]
  else:
    return None

def decrease(value, by=1):
  return value - by

def serialize(obj):
  """Return json for <instances of commons.models.Redis>
  """
  if isinstance(obj, Redis):
    return json.dumps(obj.as_dict())
  elif type(obj) == list:
    return '[%s]'%','.join(map(lambda i: json.dumps(i.as_dict) if isinstance(obj, Redis) else json.dumps(i), obj))
  elif type(obj) == dict:
    return '{%s}'%','.join(map(lambda i: '"%s": %s'%(i[0], serialize(i[1])), obj.items()))
  else:
    return json.dumps(obj)