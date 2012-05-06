#!/usr/bin/env python
import sys
import downloader
import netutil
import api.S3 as s3
import os
import urlparse


gm = downloader.gm
BUCKET = downloader.BUCKET

local = netutil.connect_to_loopback()


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
  elif cmd == 'update':
    local_update()
  elif cmd == "delete":
    delete(sys.argv[2])
  elif cmd == 'nuke_from_orbit' or cmd == 'burn_it_with_fire':
    print "It's the only way to be sure"
    delete("")
  else:
    print "Invalid subcommand"
    print "Usage: lan$ list"
    print "Usage: lan$ get <file>"
    print "Usage: lan$ add <filename>"
    print "This service is powered by $$$ :D"
    sys.exit(2)

def local_update():
  local.local_update()

def do_list():
  for e in gm.list_bucket(BUCKET).entries:
    print e.key, ':', e.size

# DEBUG ONLY
def delete(prefix):
  for e in gm.list_bucket(BUCKET).entries:
    if e.key.startswith(prefix):
      gm.delete(BUCKET, e.key)

STATUS = 0
PAYLOAD = 1

def locateall():
  for e in gm.list_bucket(BUCKET).entries:
    place = locate(e.key)
    print '%-10s %6d    %s' % (e.key, e.size, place)

def locate(filename):
  target = os.path.join(os.path.dirname(__file__), "data", filename)
  if os.path.exists(target):
    return 'local'

  next = local
  while next is not None:
    res = next.route(filename)
    if res[STATUS] == 'DATA':
      return urlparse.urlparse(res[PAYLOAD][0]).hostname
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
    return

  next = local
  while next is not None:
    res = next.route(filename)
    if res[STATUS] == 'DATA':
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
  print filename
  with open(filename) as f:
    gm.put(BUCKET, os.path.basename(filename), f)
    if not os.path.exists(os.path.join("data", os.path.basename(filename))):
      os.link(filename, os.path.join("data", os.path.basename(filename)))


if __name__ == "__main__":
  main()

