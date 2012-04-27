import db
from os import listdir
from os.path import isfile, join
import netutil


class Server(object):
  def __init__(self, parent):
    self.db = db.DB()
    self.parent = parent

  def join(self, db):
    self.db.addDb(db)

  def ping(self, uuid):
    # check for file here
    return True

  def route(self, uuid):
    try:
      return ("DATA", self.db.find(uuid))
    except KeyError:
      if self.parent is not None:
        return ("NEXT", self.parent)
      else:
        return ("BAD", None)

parent = gm.suggest() # FIXME

s = Server(parent)

rpcs = netutil.LocalMasterServer()
rpcs.register(s.join);
rpcs.register(s.add);
rpcs.register(s.route);
rpcs.register(s.ping);
rpcs.register(s.list);

rpcs.start()

gm = netutil.connect_or_die().grand_master


def get_local_files():
  """ gets a { UUID : URL }
  """
  # FIXME
  onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

while True:
  parent.join(get_local_files())
  # sleep(1000)
