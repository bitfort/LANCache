#!/usr/bin/env python
import sys
import downloader
import netutil.netapi
import api.S3 as s3
import os

server = netutil.netapi.connect_or_die()

local = server.local_master

gm = s3.AWSAuthConnection("AKIAI5C3B4IPLZDLBPKA", "QAzLIUIATfMX3JnxzrKm5Xd3YWB6k5tTxle0U22B")
BUCKET = "capel_bittorf"

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
    print "Usage: lan$ get <file>"
    print "Usage: lan$ add <filename>"
    print "This service is powered by $$$ :D"
    sys.exit(2)

def do_list():
  for e in gm.list_bucket(BUCKET).entries:
    print e.key, ':', e.size

STATUS = 0
PAYLOAD = 1

def get(filename):

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
      target = os.path.join(os.path.dirname(__file__), "data", filename)
      if os.path.exists(target):
        print "Local file exists, please move it first"
        return
      obj = gm.get(BUCKET, filename)
      if obj.message != "200 OK":
        print "Bad filename, message:"
        print obj.message
        return
      with open(target, 'w') as f:
        f.write(obj.object.data)
      return

    else:
      print res
      print "?!?"

def add(filename):
  with open(filename) as f:
    gm.put(BUCKET, filename, f)

main()

