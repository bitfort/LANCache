import sys
import time

import chubby
import filesys


start = time.time()
tag = sys.argv[1]
print 'Producing : ', tag


BIG_DATA = 'x'*1024*1024*2

for i in xrange(6):
  name = '{0}-{1}-{2}'.format(tag, start, i)
  print name, time.time(),
  f = filesys.open_(name, 'w')
  print time.time(),
  f.write(BIG_DATA)
  print time.time()
  f.close()
  chubby.push('testq', name)


