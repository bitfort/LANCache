import sys
import time

import chubby
import filesys


start = time.time()
tag = sys.argv[1]
print 'Consuming ' 


for i in xrange(5):
  name = chubby.pull('testq', name)
  print name, time.time(),
  f = filesys._open(name, 'w')
  print time.time(),
  f.read()
  print time.time()
  f.close()
