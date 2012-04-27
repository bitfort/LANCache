import threading
import urllib


class Downloader(threading.Thread):
  def __init__(self, url):
    super(Downloader, self).__init__()
    self.url = url

  def run(self):
    urllib.urlretrieve(res[PAYLOAD][0])
