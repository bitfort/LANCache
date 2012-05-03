#!/usr/bin/env python
import netutil
import time

chubby = netutil.connect_to_gm()

finger = netutil.get_finger_print()

SLEEP = 1

def push(q, x):
  chubby.push(q, finger, x)

def pull(q):
  return chubby.pull(q, finger)

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
