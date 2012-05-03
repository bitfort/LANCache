# Victor Bittorf (bittorf@cs.wisc.edu)
# David Capel (capel@cs.wisc.edu)
"""
Types used in RPC
"""


import traceback
import threading
import collections as collect
import xmlrpclib
import rpcutil
import json
from SimpleXMLRPCServer import SimpleXMLRPCServer


class BadIdeaException(Exception): pass


class RPCHandle(object):
  def __init__(self, host=None, port=None, RPC=None):
    self.host = host
    self.port = port
    self.d = {'RPC':'flag', 'host' : self.host, 'port' : self.port}
    self.__connect()

  def __connect(self):
    url = "http://{0}:{1}/".format(self.host, self.port)
    print 'Connecting to ', url
    self.proxy = xmlrpclib.ServerProxy(url, allow_none=True) 

  def __getattr__(self, name):
#    print self, ' :: ', name
    def __(*args):
      neuargs = []
      for arg in args:
        if type(arg) is RPCHandle:
          neuargs.append(arg.d)
        else:
          neuargs.append(arg)
      print 'Remote Calling: ', self, name, 'with', neuargs
      rval = getattr(self.proxy, name)(*neuargs)
      l = []
      if type(rval) is list:
        for arg in rval:
          if (type(arg) is dict )and('RPC' in arg):
            l.append(RPCHandle(**arg))
          else:
            l.append(arg)
        return l
      return rval
    return __

  @classmethod
  def decode(cls, j):
#    print '*** DECODE **'
    return RPCHandle(j['host'], j['port'])

  def __str__(self):
    return 'RPCHandle<{0}:{1}>'.format(self.host, self.port)


def _guard(hook):
  def __(*args):
    neuargs = []
    for arg in args:
      if type(arg) is RPCHandle:
        raise BadIdeaException('don\'t pass RPC objects upstream')
      if type(arg) is dict and 'RPC' in arg:
        neuargs.append(RPCHandle.decode(arg))
      else:
        neuargs.append(arg)
#    print 'Invoking ', hook, ' with', neuargs
    try:
      r = hook(*neuargs)
      l = []
      if type(r) is list or type(r) is tuple:
        for arg in r:
          if type(arg) is RPCHandle:
            l.append(arg.d)
          else:
            l.append(arg)
        return l
      else:
        return r

    except Exception, e:
      traceback.print_exc()
      print e
      raise SystemExit
    return None
  return __


class RPCServer(threading.Thread):
  def __init__(self, port, host='localhost'):
    threading.Thread.__init__(self)
    super(threading.Thread, self).__init__()
    self.port = port
    print 'Starting: ', host, port
    self.server = SimpleXMLRPCServer((host, port), allow_none=True)

  def register(self, hook, name=None):
    if name is None:
      name = hook.func_name
    hook = _guard(hook)
    print 'Register: ', name, ' to ', hook
    self.server.register_function(hook, name)

  def run(self):
    print "Starting on port", self.port
    self.server.serve_forever()
