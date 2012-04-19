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
    self.__gm_ref = rpcutil.RPC_REF(*conf.grand_master)
    self.__local_ref = rpcutil.RPC_REF(*conf.local_master)

  def _connect(self):
    self.grand_master = rpcutil.connect_to_server(self.__gm_ref)
    self.local_master = rpcutil.connect_to_server(self.__local_ref)
    
  
def connect():
  conf = netconf.load_conf()
  nl = NetLayer(conf)
  nl._connect()
  return nl


def connect_or_die():
  try:
    return connect()
  except Exception, e:
    print e
    raise SystemExit
