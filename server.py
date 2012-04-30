import db
from os import listdir
from os.path import isfile, join
import netutil
from netutil import as_url
from time import sleep
from optparse import OptionParser


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

parent = netutil.connect_to_parent()

print 'Found a parent' , parent


parser = OptionParser()
parser.add_option("-a", "--annonuce", dest="announce",action="store_true",
                      help="Lets this server parent other's", metavar="ANNOC")

(options, args) = parser.parse_args()

s = Server(parent)

gm = netutil.connect_or_die().grand_master

rpcs = netutil.LocalMasterServer()
rpcs.register(s.join);
rpcs.register(s.route);

rpcs.start()

def get_local_files(path):
  """ gets a { UUID : URL }
  """
  return { f:as_url(f) for f in listdir(path) if isfile(join(path,f)) }

try:
  while True:
    # remind the GM that we are a masta
    if options.announce:
      netutil.announce()
    

    files = get_local_files("data")
    print files, ' < < '
    if not files:
      sleep(1)
      continue
    s.join(files)
    if parent:
      parent.join(files)
    sleep(10)
except (Exception, KeyboardInterrupt), e:
  print e
  print '-- Exiting.'
  rpcs._Thread__stop()
  raise SystemExit
