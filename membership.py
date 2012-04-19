import db


class Server(object):
  def __init__(self):
    self.db = db.db()
    self.parent = None

  def join(self, child, uuids):
    self.db.addChild(child, uuids)

  def ping(self, uuid):
    # check for file here
    return True

  def add(self, uuid, url):
    # blah
    pass

  def route(self, uuid):
    try:
      while True:
        child = self.db.find(uuid)
        if child.find(uuid).query(uuid):
          return ("DATA", child)
        else:
          self.db.remove(child, uuid)
    except KeyError:
      if parent is not None:
        return ("NEXT", self.parent)
      else:
        return ("BAD", None)

