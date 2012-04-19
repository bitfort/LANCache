# Victor Bittorf (bittorf@cs.wisc.edu)
# David Capel (capel@cs.wisc.edu)
"""
Types used in RPC
"""


import collections as collect
import xmlrpclib
import rpcutil
from SimpleXMLRPCServer import SimpleXMLRPCServer


RPC_REF = collect.namedtuple('RPC_REF', ['host', 'port'])


def connect_to_server(rpcref):
  assert type(rpcref) == rpcutil.RPC_REF
  proxy = xmlrpclib.ServerProxy("http://{0}:{1}/".format(rpcref.host, 
                                                         rpcref.port)) 
  proxy.rpcref = rpcref
  return Morph(proxy)


class Morph(object):
  def __init__(self, delegate):
    self.delegate = delegate

  def __getattr__(self, name):
    return Morph(getattr(self.delegate, name))

  def __call__(self, *args):
    r = self.delegate(*args)
    if type(r) == rpcutil.RPC_REF:
      return connect_to_server(r)
    return r
