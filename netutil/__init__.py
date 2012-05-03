""" 
Main top level package
"""
import socket
import rpcutil
import netconf
import nettool

RPCServer = rpcutil.RPCServer
RPCHandle = rpcutil.RPCHandle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
HOST = s.getsockname()[0]
s.close()

conf = netconf.load_conf()
FINGER_PRINT = None

print 'You are ', HOST

def connect_to_gm():
  return rpcutil.RPCHandle(*conf.grand_master)


def connect_to_loopback():
  return rpcutil.RPCHandle(HOST, conf.local_master[1])


class GrandMasterServer(RPCServer):
  def __init__(self):
    conf = netconf.load_conf()
    super(GrandMasterServer, self).__init__(conf.grand_master[1],
        host=conf.grand_master[0])


class LocalMasterServer(RPCServer):
  def __init__(self):
    conf = netconf.load_conf()
    super(LocalMasterServer, self).__init__(conf.local_master[1], host=HOST)

#HOST = socket.gethostbyname(socket.gethostname())

def as_url(basename):
  conf = netconf.load_conf()
  return 'http://{0}:{1}/{2}'.format(HOST, conf.port, basename)

def get_finger_print():
  if not FINGER_PRINT:
    FINGER_PRINT = nettool.get_raw_trace()[0]
  return FINGER_PRINT

def connect_to_parent():
  trace = nettool.get_raw_trace()
  print '*** Trace Route ***'
  print trace 
  print 
  parent = connect_to_gm().suggest(trace)
  if parent is None:
    return None
  return RPCHandle(parent[0], parent[1])

def announce():
  gm = connect_to_gm()
  trace = nettool.get_raw_trace()
  lm = netconf.load_conf().local_master
  lm = (HOST, lm[1])
  gm.announce(lm, trace)
