
import netutil
import xmlrpclib


serv1 = netutil.LocalMasterServer()



def delegate(obj):
  return obj.foo()
serv1.register(delegate)
serv1.start()


layer = netutil.connect_or_die()

grand = layer.grand_matser
local = layer.local_master



print 'grand master foo:'
print grand.foo()

print 'local foo delegate:'
print local.delegate(grand)



