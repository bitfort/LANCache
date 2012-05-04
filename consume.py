import sys
import time

import chubby
import filesys


start = time.time()
tag = sys.argv[1]
print 'Consuming ' 

def consume(name):
  print name, time.time(),
  f = filesys.open_(name, 'w')
  print time.time(),
  f.read()
  print time.time()
  f.close()


chubby.consume_all('testq', consume)
