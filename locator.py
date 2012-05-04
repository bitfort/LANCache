

import time
import netutil
import collections


LEASE = 60

gm = netutil.GrandMasterServer()


MAP = collections.defaultdict(lambda: None)
Qs = collections.defaultdict(lambda: 
    collections.defaultdict(lambda: []))


def suggest(trace):
  part = str(trace)
  parent = MAP[part]
  if parent is None:
    print 'SUGGEST: {0} => None'.format(part)
  else:
    parent = parent[0]
    print 'SUGGEST: {0} => {1[0]}:{1[1]}'.format(part, parent)
  return parent


def announce( (host, port), trace):
  print 'ANNOUNCE: {0}:{1} for {2}'.format(host, port, trace) 
  MAP[str(trace)] = ((host, port), time.time() + LEASE)

def push(qname, net, value):
  print Qs
  net = str(net)
  print 'push for: ', net
  print Qs[qname][net]
  l =  Qs[qname][net]
  print l, value
  l.append(value)

def pull(qname, net):
  print Qs
  net = str(net)
  print 'Pull for: ', net
  if len(Qs[qname][net]) > 0:
    print 'Hit local!'
    v = Qs[qname][net].pop(0)
    print 'Got :', v
    return v
  else:
    print 'Nothing in local queue'
    for k in Qs[qname].keys():
      if len(Qs[qname][k]) > 0:
        print 'Found something for: ', k
        return Qs[k].pop(0)
  print 'Found nothing for you.'
  return None


gm.register(suggest)
gm.register(announce)
gm.register(push)
gm.register(pull)

gm.start()

try:
  while True:
    for i in xrange(6):
      print MAP
      time.sleep(10)
    nao = time.time()
    bad = filter(lambda k: MAP[k][1] < nao, MAP.keys())
    for b in bad:
      print 'Expire: ', b
      del MAP[b]
except KeyboardInterrupt:
  print '-- Exiting.'
  gm._Thread__stop()
  raise SystemExit


print '----------------- WHAT?'
gm._Thread__stop()
raise SystemExit
