import sys
import time

import chubby
import filesys


start = time.time()
tag = sys.argv[1]
print 'Producing : ', tag


BIG_DATA = 'eightbyt'*1024

for i in xrange(5):
  name = '{0}-{1}-{2}'.format(tag, start, i)
  f = filesys._open(name, 'w')
  f.write(BIG_DATA)
  f.close()
  chubby.push('testq', name)



