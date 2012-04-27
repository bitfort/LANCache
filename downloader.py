import threading
import urllib
import os.path as path


class Downloader(threading.Thread):
  def __init__(self, url):
    super(Downloader, self).__init__()
    self.url = url

  def run(self):
    dir_ = path.dirname(__file__)
    base = path.basename(self.url)
    target = path.join(dir_, 'data', base)
    print 'Downloading ', self.url, ' to', target
    urllib.urlretrieve(self.url, target)
