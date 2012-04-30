

import time
import netutil
import collections


LEASE = 60

gm = netutil.GrandMasterServer()


MAP = collections.defaultdict(lambda: None)


def suggest(trace):
  part = str(trace[0])
  parent = MAP[part]
  if parent is None:
    print 'SUGGEST: {0} => None'.format(part)
  else:
    parent = parent[0]
    print 'SUGGEST: {0} => {1[0]}:{1[1]}'.format(part, parent)
  return parent
  


def announce( (host, port), trace):
  print 'ANNOUNCE: {0}:{1} for {2}'.format(host, port, trace[0]) 
  MAP[str(trace[0])] = ((host, port), time.time() + LEASE)


gm.register(suggest)
gm.register(announce)

gm.start()

try:
  while True:
    time.sleep(70)
    nao = time.time()
    bad = filter(lambda k: MAP[k] < nao, MAP.keys())
    for b in bad:
      print 'Expire: ', b
      del MAP[b]
except KeyboardInterrupt:
  print '-- Exiting.'
  gm._Thread__stop()
  raise SystemExit

