#!/usr/bin/env python
import sys
import downloader
import netutil.netapi
import api.S3 as s3
import os

server = netutil.netapi.connect_or_die()

gm = downloader.gm
BUCKET = downloader.BUCKET

local = server.local_master

def main():
  cmd = sys.argv[1]
  if cmd == "list":
    do_list()
  elif cmd == "get":
    get(sys.argv[2])
  elif cmd == "add":
    add(sys.argv[2])
  elif cmd == 'locateall':
    locateall()
  else:
    print "Invalid subcommand"
    print "Usage: lan$ list"
    print "Usage: lan$ get <file>"
    print "Usage: lan$ add <filename>"
    print "This service is powered by $$$ :D"
    sys.exit(2)

def do_list():
  for e in gm.list_bucket(BUCKET).entries:
    print e.key, ':', e.size

STATUS = 0
PAYLOAD = 1

def locateall():
  
  for e in gm.list_bucket(BUCKET).entries:
    print '%-10s %6d    %s' % (e.key, e.size, locate(e.key))

def locate(filename):
  target = os.path.join(os.path.dirname(__file__), "data", filename)
  if os.path.exists(target):
    return 'local'

  next = local
  while next is not None:
    res = next.route(filename)
    if res[STATUS] == 'DATA':
      return str(next)
    elif res[STATUS] == 'NEXT':
      next = res[PAYLOAD]
      continue
    # get from S3
    elif res[STATUS] == 'GM':
      return 'Cloud'
    else:
      return '--Unkown?'

def get(filename):
  target = os.path.join(os.path.dirname(__file__), "data", filename)
  if os.path.exists(target):
    print "Already have it."
    return

  next = local
  while next is not None:
    res = next.route(filename)
    print res
    if res[STATUS] == 'DATA':
      print res
      downloader.Downloader(res[PAYLOAD][0]).run()
      return
    elif res[STATUS] == 'NEXT':
      next = res[PAYLOAD]
      continue
    # get from S3
    elif res[STATUS] == 'GM':
      if os.path.exists(target):
        print "Local file exists, please move it first"
        return
      downloader.CloudDownloader(filename).run()
      return

    else:
      print res
      print "?!?"

def add(filename):
  with open(filename) as f:
    gm.put(BUCKET, filename, f)


if __name__ == "__main__":
  main()

