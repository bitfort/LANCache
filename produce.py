import sys
import time

import chubby
import filesys


start = time.time()
tag = sys.argv[1]
print 'Producing : ', tag


BIG_DATA = 'eightbyt'*1024*64

for i in xrange(5):
  name = '{0}-{1}-{2}'.format(tag, start, i)
  print name, time.time(),
  f = filesys.open_(name, 'w')
  print time.time(),
  f.write(BIG_DATA)
  print time.time()
  f.close()
  chubby.push('testq', name)


# ghetto sleep.
time.sleep(100)
