import random

class DB(object):
  def __init__(self):
    self.idx = {}

  def list(self):
    return self.idx.keys()

  def addDb(self, db):
    for (k,v) in db.items():
      self.add(k, v)

  def add(self, uuid, url):
    try:
      self.idx[uuid].add(url)
    except KeyError:
      self.idx[uuid] = {url}

  #def remove(self, uuid, url):
  #  self.idx[uuid].remove(url)

  def find(self, uuid):
    return list(self.idx[uuid])
