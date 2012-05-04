import sys
import time

import chubby
import filesys


start = time.time()
print 'Consuming ' 


for i in xrange(5):
  name = chubby.pull('testq')
  print name, time.time(),
  f = filesys.open_(name, 'r')
  print time.time(),
  f.read()
  print time.time()
  f.close()
