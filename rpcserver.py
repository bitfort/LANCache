"""
Membership data. 
"""

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
  return 'NO FUCKING WAY'
  return n%2 == 0




class RPCServer(object):
  def __init__(self, port):
    self.port = port
    self.server = SimpleXMLRPCServer(("localhost", port))

  def register(self, hook):
    self.server.register_function(hook, hook.func_name)

  def serve_forever(self):
    self.server.serve_forever()


s = RPCServer(8080)
s.register(is_even)
s.serve_forever()
