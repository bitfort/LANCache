import db
from os import listdir
from os.path import isfile, join
import netutil
from netutil import as_url
from time import sleep
from optparse import OptionParser
import traceback


class Server(object):
  def __init__(self, parent):
    self.db = db.DB()
    self.parent = parent

  def join(self, db):
    self.db.addDb(db)

  def route(self, uuid):
    print 'Route Called:', uuid
    try:
      my = self.db.find(uuid)
      print 'Route returns: ', my
      return ("DATA", my)
    except KeyError:
      if self.parent is not None:
        print 'Route returns: => parent', self.parent
        return ("NEXT", self.parent)
      else:
        # download for ourself, for later?
        return ("GM", None)

parser = OptionParser()
parser.add_option("-a", "--annonuce", dest="announce",action="store_true",
                      help="Lets this server parent other's", metavar="ANNOC")

(options, args) = parser.parse_args()
parent = netutil.connect_to_parent()

print 'Found a parent' , parent



s = Server(parent)


def get_local_files(path):
  """ gets a { UUID : URL }
  """
  return { f:as_url(f) for f in listdir(path) if isfile(join(path,f)) }

def local_update():
    files = get_local_files("data")
    print files, ' < < '
    if not files:
      return
    s.join(files)
    if parent:
      parent.join(files)

rpcs = netutil.LocalMasterServer()
rpcs.register(s.join);
rpcs.register(s.route);
rpcs.register(local_update)

rpcs.start()

try:
  while True:
    # remind the GM that we are a masta
    if options.announce:
      netutil.announce()
    
    local_update()
    sleep(10)
except (Exception, KeyboardInterrupt), e:
  print e
  traceback.print_exc()
  print '-- Exiting.'
  rpcs._Thread__stop()
  raise SystemExit
