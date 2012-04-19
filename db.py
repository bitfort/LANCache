import random

class Database(object):
  def __init__(self):
    self.ridx = {}
    self.idx = {}
  def addChild(self, child, uuids):
    for uuid in uuids:
      try:
        self.ridx[uuid].add(child)
      except KeyError:
        self.ridx[uuid] = {child}

    self.idx[child] = uuids

  def leaveChild(self, child):
    for uuid in self.idx[child]:
      self.ridx[uuid].remove(child)

    del self.idx[child]

  def find(uuid):
    try:
      return random.sample(self.ridx[uuid], 1)[0]
    except KeyError:
      return None

