import db
from os import listdir
from os.path import isfile, join
import netutil
from netutil import as_url
from time import sleep


class Server(object):
  def __init__(self, parent):
    self.db = db.DB()
    self.parent = parent

  def join(self, db):
    self.db.addDb(db)

  def route(self, uuid):
    try:
      return ("DATA", self.db.find(uuid))
    except KeyError:
      if self.parent is not None:
        return ("NEXT", self.parent)
      else:
        return ("GM", None)

parent = None 

s = Server(parent)

rpcs = netutil.LocalMasterServer()
rpcs.register(s.join);
rpcs.register(s.route);

rpcs.start()

def get_local_files(path):
  """ gets a { UUID : URL }
  """
  return { f:as_url(f) for f in listdir(path) if isfile(join(path,f)) }

while True:
  files = get_local_files("data")
  print files
  if not files:
    continue
  s.join(files)
  if parent:
    parent.join(files)
  sleep(10000)
