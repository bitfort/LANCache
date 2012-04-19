"""
RPC and morph magic.
"""

import xmlrpclib
import rpctypes
from SimpleXMLRPCServer import SimpleXMLRPCServer


def connect_to_server(rpcref):
  assert type(rpcref) == rpctypes.RPC_REF
  proxy = xmlrpclib.ServerProxy("http://{0}:{1}/".format(rpcref.host, 
                                                         rpcref.port)) 
  return Morph(proxy)


class Morph(object):
  def __init__(self, delegate):
    self.delegate = delegate

  def __getattr__(self, name):
    return Morph(getattr(self.delegate, name))

  def __call__(self, *args):
    r = self.delegate(*args)
    if type(r) == rpctypes.RPC_REF:
      return connect_to_server(r)
    return r


  
