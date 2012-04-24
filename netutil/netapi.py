# Victor Bittorf (bittorf@cs.wisc.edu)
# David Capel (capel@cs.wisc.edu)
""" 
API for upper layer to use
"""


import netconf 
import rpcutil


class NetLayer(object):
  def __init__(self, conf):
    self.conf = conf

  def _connect(self):
    self.grand_master = rpcutil.RPCHandle(*self.conf.grand_master)
    self.local_master = rpcutil.RPCHandle(*self.conf.local_master)
    
  
def connect():
  conf = netconf.load_conf()
  nl = NetLayer(conf)
  nl._connect()
  return nl


def connect_or_die():
  try:
    return connect()
  except Exception, e:
    print 'Failed to Connect:'
    print e
    raise e
