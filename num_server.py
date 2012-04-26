
import netutil
import xmlrpclib

PORT = 8898

serv0 = netutil.GrandMasterServer()


def foo():
  return 55

serv0.register(foo)
serv0.run()
