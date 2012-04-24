""" 
Main top level package
"""

import netapi
import rpcutil
import netconf

RPCServer = rpcutil.RPCServer
connect_or_die = netapi.connect_or_die
RPCHandle = rpcutil.RPCHandle


class GrandMasterServer(RPCServer):
  def __init__(self):
    conf = netconf.load_conf()
    super(GrandMasterServer, self).__init__(conf.grand_master[1])

class LocalMasterServer(RPCServer):
  def __init__(self):
    conf = netconf.load_conf()
    super(LocalMasterServer, self).__init__(conf.local_master[1])
