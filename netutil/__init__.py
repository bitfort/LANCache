""" 
Main top level package
"""
import socket
import netapi
import rpcutil
import netconf
import nettool

RPCServer = rpcutil.RPCServer
connect_or_die = netapi.connect_or_die
RPCHandle = rpcutil.RPCHandle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
HOST = s.getsockname()[0]
s.close()

print 'You are ', HOST


class GrandMasterServer(RPCServer):
  def __init__(self):
    conf = netconf.load_conf()
    super(GrandMasterServer, self).__init__(conf.grand_master[1])

class LocalMasterServer(RPCServer):
  def __init__(self):
    conf = netconf.load_conf()
    super(LocalMasterServer, self).__init__(conf.local_master[1])

#HOST = socket.gethostbyname(socket.gethostname())

def as_url(basename):
  conf = netconf.load_conf()
  return 'http://{0}:{1}/{2}'.format(HOST, conf.port, basename)


def connect_to_parent():
  trace = nettool.get_raw_trace()
  print '*** Trace Route ***'
  print trace 
  print 
  parent = connect_or_die().grand_master.suggest(trace)
  if parent is None:
    return None
  return RPCHandle(parent[0], parent[1])

def announce():
  gm = connect_or_die().grand_master
  trace = nettool.get_raw_trace()
  lm = netconf.load_conf().local_master
  lm = (HOST, lm[1])
  gm.announce(lm, trace)
