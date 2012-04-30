#!/usr/bin/env python
import netutil
import time

server = netutil.connect_or_die()
chubby = server.grand_master

finger = netutil.get_finger_print()

SLEEP = 1

def produce_all(q, gen):
  for x in gen:
    chubby.push(q, finger, x)

def consume_all(q, con):
  while True:
    x = chubby.pull(q, finger)
    if x:
      con(s)
    else:
      sleep(SLEEP)
