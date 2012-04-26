#!/usr/bin/env python
import sys
import urllib
import netutil.netapi

server = netutil.netapi.connect_or_die()

local = server.local_master

def main():
  cmd = sys.argv[1]
  if cmd == "list":
    do_list()
  elif cmd == "get":
    get(sys.argv[2])
  elif cmd == "add":
    add(sys.argv[2])
  else:
    print "Invalid subcommand"
    print "Usage: lan$ list"
    print "Usage: lan$ get <uuid>"
    print "Usage: lan$ add <filename>"
    print "This service is powered by $$$ :D"
    sys.exit(2)


def do_list():
 print local.list() 

STATUS = 0
PAYLOAD = 1

def get(uuid):
  next = local
  while next is not None:
    res = next.route(uuid)
    print res
    if res[STATUS] == 'DATA':
      print res
      urllib.urlretrieve(res[PAYLOAD][0])
      return
    elif res[STATUS] == 'NEXT':
      next = res[PAYLOAD]
      continue
    elif res[STATUS] == 'BAD':
      print "Bad UUID"
      return
    else:
      print 'Bad status ' + str(res[STATUS])
  print "Ok."

def add(filename):
  local.add(filename, filename)

main()
