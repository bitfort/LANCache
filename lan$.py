#!/usr/bin/env python
import sys
import urllib
import netutil.netapi

server = netutil.netapi.connect_or_die()

local = server.local_master
gm = server.grand_master

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
 print gm.list() 

def get(uuid):
  next_server = local
  while next is not None:
    res = next.route(uuid)
    if res['status'] == 'DATA':
      curl.get(res['payload'])
      urllib.urlretrieve(res['payload'], api.base + uuid)
    elif res['status'] == 'NEXT':
      next_server = res['payload']
      continue
    elif res['status'] == 'BAD':
      print "Bad UUID"
    else:
      print 'Bad status ' + str(res['status'])
  print "Ok."

def add(filename):
  print "uploading filename!!!!"
