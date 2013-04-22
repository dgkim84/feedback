# -*- coding: utf-8 -*-
from feedback import db

import json

class RedisType(type):
  def __new__(meta, name, bases, attrs):
    return type.__new__(meta, name, bases, attrs)

  def __getattr__(cls, name):
    if name.lower() in ['get', 'hget', 'hmget', 'set', 'hset', 'hmset'
        , 'ttl', 'expire', 'setnx', 'incr', 'hincrby', 'pipeline'
        , 'delete'
        , 'zrevrangebyscore', 'zrangebyscore']:
      return getattr(db, name.lower())
    elif hasattr(cls, name):
      return getattr(cls, name)
    raise AttributeError(key)

class Redis:
  __metaclass__ = RedisType

  value = {}

  @classmethod
  def make_unique_index(cls, item, index='id'):
    """중복되지 않도록 유지하기 위함
    """
    return (int(item[index]) << 32) | item['id']

  @classmethod
  def all(cls, num = 20, max_id = float('inf'), index='id', order='desc', part=None, **kwargs):
    prefix = cls.__namespace__
    if part in cls.__partitions__ and kwargs.get(part) is not None:
      prefix = '%s:part:%s:%s'%(prefix, part, kwargs.get(part))
    if index in cls.__indexes__:
      prefix = '%s:index:%s'%(prefix, index)
    else:
      prefix = '%s:index:id'%(prefix)

    if order == 'desc':
      all = cls.zrevrangebyscore(prefix, max_id, 0, 0, num)
    else:
      all = cls.zrangebyscore(prefix, 0, max_id, 0, num)
    if all:
      return map(lambda i: json.loads(i), cls.hmget('%s:rows'%cls.__namespace__, all))
    else:
      return []

  @classmethod
  def get_by_id(cls, id):
    """Return object by id.

    :returns: object corresponding to id
    :rtype: object
    """
    value = cls.hget('%s:rows'%cls.__namespace__, id)
    if value:
      return cls(**json.loads(value))
    return None

  def next_id(self):
    """Return next sequence id.

    :returns: next sequence
    :rtype: string
    """
    return Redis.incr('%s:sequence'%(self.__namespace__))

  def __init__(self, *args, **kwargs):
    self.value = kwargs
    if not self.value.has_key('id'):
      self.value['id'] = None

  def as_dict(self):
    """Return as dict"""
    return self.value

  def save(self):
    """Save the object

    등록된 파티션키/값, 인덱스 정보를 바탕으로 key를 복제하여 조회할 때 사용한다.
    
    indexes = ['id'] 이고 partitions = ['project'] 이고
      project id가 P1인 객체를 등록하면 다음 키에 데이터를 넣는다.

    단, 해당 index/part 값이 None인 경우는 염두하지 않았음을 밝힘.

    NS:rows
    NS:index:id
    NS:part:project:P1:index:id
    """
    id = self.as_dict().get('id')
    if not id:
      id = self.next_id()
      self.as_dict()['id'] = id

    p = db.pipeline()
    p.hset('%s:rows'%self.__namespace__, str(id), json.dumps(self.value))
    for index in self.__indexes__:
      key = '%s:index:%s'%(self.__namespace__, index)
      p.zadd(key, self.make_unique_index(self.as_dict(), index), id)

    for part in self.__partitions__:
      for index in self.__indexes__:
        key = '%s:part:%s:%s:index:%s'%(self.__namespace__, part, 
          self.as_dict()[part], index)
        p.zadd(key, self.make_unique_index(self.as_dict(), index), id)
    p.execute()

  def delete(self):
    """Delete the object"""
    if not hasattr(self, 'id'):
      return False
    this = cls.hget('%s:rows'%cls.__namespace__, id)
    if not this:
      return False
    this = json.loads(this)
    p = db.pipeline
    p.hdel('%s:rows'%self.__namespace__, str(id))
    p.zrem('%s:index'%self.__namespace__, id)
    if self.__indexes__:
      for index in self.__indexes__:
        if this.has_key(index):
          p.zrem('%s:index:%s'%(self.__namespace__, this[index]), id)
    if self.__partitions__:
      for part in self.__partitions__:
        if this.has_key(part):
          p.zrem('%s:part:%s'%(self.__namespace__, this[part]), id)
    res = p.execute
    return res[0]

  def __getattr__(self, name):
    if hasattr(self, name):
      return self.__dict__[name]
    return self.value[name]

  def __hasattr__(self, name):
    if hasattr(self, name):
      return True
    return hasattr(self.value, name)

  def __setattr__(self, name, value):
    if hasattr(self, name):
      self.__dict__[name] = value
    else:
      self.value[name] = value