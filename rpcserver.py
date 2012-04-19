"""
Membership data. 
"""

import xmlrpclib
import rpctypes
from SimpleXMLRPCServer import SimpleXMLRPCServer


def is_even(n):
  return 'NO FUCKING WAY'
  return n%2 == 0


def serialize_rpc_wrap(hook):
  def __(*args):
    r = hook(*args)
    if type(arg) is rpctypes.Morph:
      r = r.delegate
    if type(r) is xmlrpc.ServerProxy:
      return r.rpcref
    return r


class RPCServer(object):
  def __init__(self, port):
    self.port = port
    self.server = SimpleXMLRPCServer(("localhost", port))

  def register(self, hook, name=None):
    if name is None:
      name = hook.func_name
    self.server.register_function(hook, name)

  def serve_forever(self):
    self.server.serve_forever()


s = RPCServer(8080)
s.register(is_even)
s.serve_forever()
