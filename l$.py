import sys
from lancache import local, master


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
    sys.exit(2)


def do_list():
 print master.list() 

def get(uuid):
  addr = local.route(uuid)
  print addr.get(uuid)

def add(filename):
  print "uploading filename!!!!"
