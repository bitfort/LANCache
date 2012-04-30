
import threading
import hashlib
import tempfile
import os
lan = __import__("lan$")

class Async(threading.Thread):
  def __init__(self, hook, *args):
    threading.Thread.__init__(self)
    self.hook = hook
    self.args = args
    self.start()
  
  def run(self):
    self.hook(*self.args)


class WriteHandle(object):
  def __init__(self, name):
    self.name = name
    self.handle = tempfile.NamedTemporaryFile()

  def write(self, buf):
    self.handle.write(buf)

  def close(self):
    target = os.path.join(os.path.dirname(__file__), "data", self.name)
    os.rename(self.handle.name, target)
    def __():
      lan.add(self.name)
      lan.local_update
    Async(__)


class ReadHandle(object):
  def __init__(self, name):
    self.name = name
    self.fullname = os.path.join(os.path.dirname(__file__), "data", self.name)
    self.flag = threading.Event();
    self.handle = None

    def __():
      lan.get(self.name)
      self.flag.set()
    Async(__)

  def read(self, *args):
    if not self.flag.is_set():
      self.flag.wait()
    if not self.handle:
      self.handle = open(self.fullname, 'r')
    return self.handle.read(*args)

  def close(self):
    if self.handle:
      self.handle.close()


def open_(name, mode='r'):
  assert mode == 'w' or mode == 'r'
  if mode == 'w':
    return WriteHandle(name)
  return ReadHandle(name)
