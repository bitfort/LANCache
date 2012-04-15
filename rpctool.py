"""
Membership data. 
"""

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

def is_even(n):
  return 'NO FUCKING WAY'
  return n%2 == 0



HOOKS = {
  'is_even' : is_even
}

def start_server(port):
  server = SimpleXMLRPCServer(("localhost", 8000))
  for name, hook in HOOKS.items():
    print 'Reg: ', name, hook
    server.register_function(hook, name)
  server.serve_forever()

start_server(8808)
