import sys
import time

import chubby
import filesys


start = time.time()
print 'Consuming ' 

def consume(name):
  print name, time.time(),
  f = filesys.open_(name, 'r')
  print time.time(),
  f.read()
  print time.time()
  f.close()


chubby.consume_all('testq', consume)
