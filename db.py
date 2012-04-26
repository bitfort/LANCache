import random

class DB(object):
  def __init__(self):
    self.idx = {}

  def addChild(self, child, uuids):
    for uuid in uuids:
      self.add(child, uuid)

  def add(self, child, uuid):
    try:
      self.idx[uuid].add(child)
    except KeyError:
      self.idx[uuid] = {child}

  def remove(self, child, uuid):
    self.idx[uuid].remove(child)

  def find(uuid):
    try:
      return random.choice(self.idx[uuid])
    except (KeyError, IndexError):
      raise KeyError
