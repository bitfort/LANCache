
import xmlrpclib
import rpctypes
from SimpleXMLRPCServer import SimpleXMLRPCServer




class Functor(object):
  def __init__(self, hook):
    self.hook = hook

  def __call__(self, *args):
    r = self.hook(*args)
    if type(r) == rpctypes.RPC_REF:
      raise # return RPC Client
    return r

  

class Morph(object):
  def __init__(delegate):
    self.delegate = delegate

  def __getattr__(self, name):
    return getattr(delegate, name)

  
