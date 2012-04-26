import db
import netutil


class Server(object):
  def __init__(self):
    self.db = db.DB()
    self.parent = None

  def join(self, db):
    self.db.addDb(db)

  def ping(self, uuid):
    # check for file here
    return True

  def add(self, uuid, url):
    self.db.add(uuid, url)

  def list(self):
    return self.db.list()

  def route(self, uuid):
    try:
      return ("DATA", self.db.find(uuid))
    except KeyError:
      if self.parent is not None:
        return ("NEXT", self.parent)
      else:
        return ("BAD", None)

s = Server()

rpcs = netutil.LocalMasterServer()
rpcs.register(s.join);
rpcs.register(s.add);
rpcs.register(s.route);
rpcs.register(s.ping);
rpcs.register(s.list);

rpcs.run()
