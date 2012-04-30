

import netutil

gm = netutil.GrandMasterServer()


def suggest(trace):
  print 'Determining parent for : '
  print trace


def announce( (host, port), trace):
  print 'Herd about: ', host, port, trace


gm.register(suggest)
gm.register(announce)

gm.run()
